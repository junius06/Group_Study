## 데이터를 엑셀로 저장

# pandas를 pd의 이름으로 불러와서 사용한다.
import pandas as pd
import os

# 데이터 프레임 생성
df = pd.DataFrame([["joohee5079@naver.com"], 
                   ["joohee6218@gmail.com"],
                   ["aaa@asdfsdf.com"]])

current_directory = os.getcwd()
file_path = os.path.join(current_directory, 'email_list.xlsx')
print("파일 저장 경로:", file_path)

print(df)
df.to_excel(r'email_list.xlsx', index=False, header=False)