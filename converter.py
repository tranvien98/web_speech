
import unicodedata

ten_number = {'không':0,'một':1,'mốt':1,'hai':2,'ba':3,'tư':4,'bốn':4,'lăm':5,'năm':5,'sáu':6,
                'bảy':7,'bẩy':7,'tám':8,'chín':9,'mười':10,'linh':0}
unit = {'mươi':10,'nghìn':1000,'trăm':100,'ngàn:':1000}
comma = {'phẩy':',','phảy':','}

def convert_string_to_numbers(sen):
    i = 0
    number = 0
    new_sen = []
    while i < len(sen):
            number = sen[i]
            if sen[i] in ten_number:
                if sen[i]  != 'năm':
                    if i+1 < len(sen) and sen[i+1] in unit:
                        if i + 2 < len(sen) and sen[i+2] in ten_number:
                            if i + 3 < len(sen) and sen[i+3] in ten_number:
                                unit_2 = ten_number[sen[i+2]] * 10 if ten_number[sen[i+2]] < 10 else 10
                                number = ten_number[sen[i]] * unit[sen[i+1]] + unit_2 + ten_number[sen[i+3]]
                                i += 4
                            elif i + 3 < len(sen) and sen[i+3] in unit:
                                if unit[sen[i+3]] == 10:
                                    number = ten_number[sen[i]] * unit[sen[i+1]] + ten_number[sen[i+2]]*10
                                    i += 4
                                else:
                                    if i + 4 < len(sen) and sen[i+4] in ten_number:
                                        unit_2 = ten_number[sen[i+4]] * 10 if ten_number[sen[i+4]] < 10 else 10
                                        if i + 5 < len(sen) and sen[i+5] in ten_number:
                                            number =    ten_number[sen[i]] * unit[sen[i+1]] + unit_2 + \
                                                        ten_number[sen[i+2]]*unit[sen[i+3]] + \
                                                        ten_number[sen[i+5]]
                                            i += 6
                                        elif i + 5 < len(sen) and sen[i+5] in unit and sen[i+6] in ten_number: 
                                            unit_2 = ten_number[sen[i+4]] * 10 if ten_number[sen[i+4]] < 10 else 10
                                            number =    ten_number[sen[i]] * unit[sen[i+1]] + unit_2 + \
                                                        ten_number[sen[i+2]]*unit[sen[i+3]] + \
                                                        ten_number[sen[i+6]]
                                            i += 7
                                        else:
                                            number = ten_number[sen[i]] * unit[sen[i+1]] + unit_2
                                            i += 6
                                    else:
                                        number = ten_number[sen[i]] * unit[sen[i+1]] + ten_number[sen[i+2]]*unit[sen[i+3]]
                                        i += 5
                            else:
                                number = ten_number[sen[i]] * unit[sen[i+1]] + ten_number[sen[i+2]]
                                i += 3
                        else:
                            number = ten_number[sen[i]] * unit[sen[i+1]]
                            i += 2
                    elif i+1 < len(sen) and sen[i+1] in ten_number:
                        # if sen[i+2] not in ten_number:
                        unit_1 = ten_number[sen[i]] if ten_number[sen[i]] < 10 else 1
                        unit_2 = ten_number[sen[i+1]] if ten_number[sen[i+1]] < 10 else 0
                        number = unit_1 * 10 + unit_2
                        i += 2
                        

                    elif i+1 < len(sen) and sen[i+1] in comma:
                        if i + 2 < len(sen) and sen[i+2] in ten_number:
                            number = str(ten_number[sen[i]]) + ',' + str(ten_number[sen[i+2]])
                            i += 3
                        else:
                            number = str(ten_number[sen[i]]) + ',' + str(0)
                            i += 3
                    else:
                        # if i+1 < len(sen) and sen[i+1] not in ten_number:
                            # number= ten_number[sen[i]]
                        i += 1
                else:
                    i += 1
            else:
                i += 1

            new_sen.append(str(number))

    return ' '.join(new_sen)

name = {'bình thuận': 'Bình Thuận', 'quảng bình': 'Quảng Bình', 'ninh bình': 'Ninh Bình',
     'tây ninh': 'Tây Ninh', 'điện biên': 'Điện Biên', 'khánh hòa': 'Khánh Hòa', 
     'bình định': 'Bình Định', 'hòa bình': 'Hòa Bình', 'quảng ngãi': 'Quảng Ngãi', 
     'phú thọ': 'Phú Thọ', 'đồng nai': 'Đồng Nai', 'hưng yên': 'Hưng Yên', 'vĩnh phúc': 'Vĩnh Phúc', 
     'tiền giang': 'Tiền Giang', 'bình dương': 'Bình Dương', 'an giang': 'An Giang', 
     'bắc giang': 'Bắc Giang', 'thanh hóa': 'Thanh Hóa', 'kon tum': 'Kon Tum', 
     'thừa thiên huế': 'Thừa Thiên Huế', 'quảng ninh': 'Quảng Ninh', 'hà tĩnh': 'Hà Tĩnh', 
     'cần thơ': 'Cần Thơ', 'trà vinh': 'Trà Vinh', 'đồng tháp': 'Đồng Tháp', 'hà giang': 'Hà Giang', 
     'lai châu': 'Lai Châu', 'thái nguyên': 'Thái Nguyên', 'yên bái': 'Yên Bái', 'kiên giang': 'Kiên Giang', 
     'vĩnh long': 'Vĩnh Long', 'đắk nông': 'Đắk Nông', 'nam định': 'Nam Định', 'lạng sơn': 'Lạng Sơn', 
     'long an': 'Long An', 'bến tre': 'Bến Tre', 'phú yên': 'Phú Yên', 'ninh thuận': 'Ninh Thuận', 
     'tuyên quang': 'Tuyên Quang', 'hà nam': 'Hà Nam', 'hải phòng': 'Hải Phòng', 'lâm đồng': 'Lâm Đồng', 
     'sóc trăng': 'Sóc Trăng', 'sơn la': 'Sơn La', 'nghệ an': 'Nghệ An', 'đà nẵng': 'Đà Nẵng', 
     'hải dương': 'Hải Dương', 'cao bằng': 'Cao Bằng', 'đắk lắk': 'Đắk Lắk', 'gia lai': 'Gia Lai', 
     'hậu giang': 'Hậu Giang', 'bắc kạn': 'Bắc Kạn', 'quảng trị': 'Quảng Trị', 'bắc ninh': 'Bắc Ninh', 
     'cà mau': 'Cà Mau', 'quảng nam': 'Quảng Nam', 'bình phước': 'Bình Phước', 'vũng tàu': 'Vũng Tàu', 
     'thái bình': 'Thái Bình', 'bạc liêu': 'Bạc Liêu', 'hà nội': 'Hà Nội', 'lào cai': 'Lào Cai', 
     'hồ chí minh': 'Hồ Chí Minh','hoa kỳ':'Hoa Kỳ','việt nam':'Việt Nam','trung quốc':'Trung Quốc',
     'lào':'Lào','cam pu chia':'Cam Pu Chia','đông nam á':'Đông Nam Á','thái bình dương':'Thái Bình Dương'}

def name_upper(sen):
    for k in name.keys():
        if k in sen:
            sen = sen.replace(k,name[k])   
    return sen 
    

# print(convert_string_to_numbers('thực hiện chỉ đạo vào sáu phẩy bảy phần trăm'.split()))    

