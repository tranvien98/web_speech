#!/usr/bin/env python3

import json
import os
import sys
import asyncio
import pathlib
import websockets
import concurrent.futures
import logging
from vosk import Model, KaldiRecognizer
import time
import wave


def process_chunk(rec, message):
    if message == '{"eof" : 1}':
        return rec.FinalResult(), True
    elif rec.AcceptWaveform(message):
        return rec.Result(), False
#        print('done')
    else:
        return rec.PartialResult(), False

async def recognize(websocket, path):
    global model
    global args
    global loop
    global pool

    rec = None
    phrase_list = None
    sample_rate = args.sample_rate
    show_words = args.show_words
    max_alternatives = args.max_alternatives

    logging.info('Connection from %s', websocket.remote_address);
    tm=0
    check_sen=''


    #audio details
    foldir = "./static/record_file"
    if not os.path.exists(foldir):
        os.makedirs(foldir)
    name_file='./static/record_file/'+str(int(time.time()))+'.wav'
    dump_fn = wave.open(name_file, "wb")
    dump_fn.setnchannels(1)
    dump_fn.setsampwidth(2)
    dump_fn.setframerate(16000)
    # try:
    while True:
        tm=tm+1
        a=b'RIFF\xb2\x0e\x04\x00WAVEfmt '
        message = await websocket.recv()
        # print(message)
        
        # if tm<3:print(a+message)
        # Load configuration if provided
        if isinstance(message, str) and 'config' in message:
            jobj = json.loads(message)['config']
            logging.info("Config %s", jobj)
            if 'phrase_list' in jobj:
                phrase_list = jobj['phrase_list']
            if 'sample_rate' in jobj:
                sample_rate = float(jobj['rate'])
                print(sample_rate)
                print()
                print()
                print()
            if 'words' in jobj:
                show_words = bool(jobj['words'])
            if 'max_alternatives' in jobj:
                max_alternatives = int(jobj['max_alternatives'])
            continue
        
        # Create the recognizer, word list is temporary disabled since not every model supports it
        if not rec:
            if phrase_list:
                rec = KaldiRecognizer(model, 16000, json.dumps(phrase_list, ensure_ascii=False))
            else:
                rec = KaldiRecognizer(model, 16000)
            rec.SetWords('True')
            rec.SetMaxAlternatives(max_alternatives)
        rec.SetWords('True')
        
        #write file audio
        dump_fn.writeframes(message)


        response, stop = await loop.run_in_executor(pool, process_chunk, rec, message)
        # if tm==1 and 'partial'in response and json.loads(response)['partial']!='': json.loads(response)['partial']=check_sen
        # if 'partial'in response and json.loads(response)['partial']==check_sen and json.loads(response)['partial']!='':
        #     json.loads(response)['partial']=check_sen
        # else: 
        # print(response)
        #if 'partial'in response: 
        res = json.loads(response)
        res["name_file"] = name_file
        # print(res)
        await websocket.send(json.dumps(res))
#        if 'partial'in response and json.loads(response)['partial']!='':print(json.loads(response)['partial'])
        # await websocket.send(response)
        if stop: break
    # except Exception as e:
    #     print(e)
    #     dump_fn.close()
    #     print('done to dump')


def start():

    global model
    global args
    global loop
    global pool

    # Enable loging if needed
    #
    # logger = logging.getLogger('websockets')
    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler())
    logging.basicConfig(level=logging.INFO)

    args = type('', (), {})()

    args.interface = os.environ.get('VOSK_SERVER_INTERFACE', '0.0.0.0')
    args.port = int(os.environ.get('VOSK_SERVER_PORT', 8080))
    args.model_path = os.environ.get('VOSK_MODEL_PATH', 'model')
    args.sample_rate = float(os.environ.get('VOSK_SAMPLE_RATE', 16000))
    args.max_alternatives = int(os.environ.get('VOSK_ALTERNATIVES', 0))
    args.show_words = bool(os.environ.get('VOSK_SHOW_WORDS', True))

    if len(sys.argv) > 1:
       args.model_path = sys.argv[1]

    # Gpu part, uncomment if vosk-api has gpu support
    #
    # from vosk import GpuInit, GpuInstantiate
    # GpuInit()
    # def thread_init():
    #     GpuInstantiate()
    # pool = concurrent.futures.ThreadPoolExecutor(initializer=thread_init)

    model = Model(args.model_path)
    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))
    loop = asyncio.get_event_loop()

    start_server = websockets.serve(
        recognize, args.interface, args.port)

    logging.info("Listening on %s:%d", args.interface, args.port)
    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == '__main__':
    start()
