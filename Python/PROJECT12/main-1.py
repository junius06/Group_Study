## 데이터를 엑셀로 저장

# pandas를 pd의 이름으로 불러와서 사용한다.
import pandas as pd
import os

# 데이터 프레임 생성
df = pd.DataFrame([["김주희", "1996.06.24", "2015.03.06"], 
                   ["아무개", "1997.06.25", "2015.03.07"],
                   ["호롱이", "1998.06.26", "2015.03.08"],
                   ["장삐쭈", "1999.06.27", "2015.03.09"]])

current_directory = os.getcwd()
file_path = os.path.join(current_directory, '수료증명단.xlsx')
print("파일 저장 경로:", file_path)

print(df)
df.to_excel(r'수료증명단.xlsx', index=False, header=False)