# Mars_Base_Inventory_List.csv 파일 읽기 및 리스트로 변환
inventory_list = []

try:
    with open('2week/Mars_Base_Inventory_List.csv', 'r') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')
        for line in lines[1:]:
            values = line.strip().split(',')
            if len(values) != len(headers):
                print('경고: 열 개수가 헤더와 일치하지 않습니다 -', line.strip())
                continue
            item_dict = {headers[i].strip(): values[i] for i in range(len(headers))}
            inventory_list.append(item_dict)
except FileNotFoundError:
    print('오류: "2week/Mars_Base_Inventory_List.csv" 파일을 찾을 수 없습니다.')
    exit(1)
except Exception as e:
    print('오류: 파일 읽기 중 문제가 발생했습니다 -', e)
    exit(1)

# 원본 화물 목록 출력
print('원본 화물 목록:')
for item in inventory_list:
    print(item)

# 인화성이 높은 순으로 정렬
try:
    sorted_inventory = sorted(
        inventory_list,
        key=lambda x: float(x['Flammability']),
        reverse=True
    )
except KeyError:
    print('오류: "Flammability" 키가 데이터에 존재하지 않습니다.')
    exit(1)
except ValueError:
    print('오류: "Flammability" 값을 숫자로 변환할 수 없습니다.')
    exit(1)

# 인화성 지수 0.7 이상인 항목 추출
dangerous_items = [
    item for item in sorted_inventory if float(item['Flammability']) >= 0.7
]

# 인화성 지수 0.7 이상인 항목 출력
print('\n인화성 지수 0.7 이상인 항목:')
for item in dangerous_items:
    print(item)

# 인화성 지수 0.7 이상인 항목을 CSV 형식으로 저장
try:
    with open('2week/result/Mars_Base_Inventory_danger.csv', 'w') as file:
        file.write('Substance,수량,인화성\n')
        for item in dangerous_items:
            line = f"{item['Substance']},N/A,{item['Flammability']}\n"
            file.write(line)
    print('\n인화성 지수 0.7 이상인 항목이 "Mars_Base_Inventory_danger.csv" 파일로 저장되었습니다.')
except KeyError as e:
    print('오류: 데이터에 필요한 키가 없습니다 -', e)
    exit(1)
except FileNotFoundError:
    print('오류: "2week/result" 디렉토리를 찾을 수 없습니다.')
    exit(1)
except Exception as e:
    print('오류: 파일 저장 중 문제가 발생했습니다 -', e)
    exit(1)

# 정렬된 배열을 이진 파일로 저장
try:
    with open('2week/result/Mars_Base_Inventory_List.bin', 'wb') as file:
        for item in sorted_inventory:
            # 딕셔너리를 문자열로 변환 후 바이트로 인코딩
            line = f"{item['Substance']},{item['Weight (g/cm³)']},{item['Specific Gravity']},{item['Strength']},{item['Flammability']}\n"
            file.write(line.encode('utf-8'))
    print('정렬된 화물 목록이 "Mars_Base_Inventory_List.bin" 이진 파일로 저장되었습니다.')
except Exception as e:
    print('오류: 이진 파일 저장 중 문제가 발생했습니다 -', e)
    exit(1)

# 이진 파일 읽기 및 출력
print('\n"Mars_Base_Inventory_List.bin"에서 읽어온 내용:')
try:
    with open('2week/result/Mars_Base_Inventory_List.bin', 'rb') as file:
        binary_content = file.read()
        # 바이트를 문자열로 디코딩하여 출력
        decoded_content = binary_content.decode('utf-8')
        for line in decoded_content.splitlines():
            print(line)
except FileNotFoundError:
    print('오류: "Mars_Base_Inventory_List.bin" 파일을 찾을 수 없습니다.')
    exit(1)
except Exception as e:
    print('오류: 이진 파일 읽기 중 문제가 발생했습니다 -', e)
    exit(1)