# JSP

> 날짜: 2026-01-29
> 원본 노션: [링크](https://www.notion.so/JSP-2f7b28703eb0804c8df1f8b166c817d1)

---

# <form>

```sql
<form action="./loginAction" method="post">
```

---

# <input>입력 박

```sql
<input>
```

### 텍스트 입력

```sql
<input type="text" name="id">
```

- 일반 문자열 입력
- name="id" → 서버에서 request.getParameter("id") 로 받음
### 비밀번호 입력

```sql
<input type="password" name="pw">
```

- 입력값이 ●●● 로 가려짐
- 실제 값은 서버로 정상 전송됨
### 숫자 입력

```sql
<input type="number">
```

- 숫자만 입력 가능
- 모바일에서는 숫자 키패드 뜸
### 이메일 입력

```sql
<input type="email">
```

- 이메일 형식 체크 (@ 포함 등)
- 틀리면 전송 안 됨
### 날짜 선택

```sql
<input type="date">
```

- 달력 UI 제공
- 생일, 일정 선택할 때 사용
### 파일 선택

```sql
<input type="file">
```

- 파일 업로드
- 서버에서는 multipart/form-data 필요
### 색상 선택

```sql
<input type="color">
```

- 색상 팔레트 제공
### 범위 선택 (슬라이더)

```sql
<input type="range" min="0" max="100">
```

- 슬라이더로 값 선택
- 볼륨, 밝기 설정 등에 사용
---

# <button>

```sql
<button></button>
```

### submit 버튼

```sql
<button type="submit">login</button>
```

- form 안에서 클릭 시 서버로 데이터 전송
### reset 버튼

```sql
<button type="reset">reset</button>
```

- 입력값 초기화
### 자바스크립트 버튼

```sql
<button onclick="location.href='https://www.naver.com/'">button</button>
```

- 클릭 시 다른 페이지로 이동
- 서버 요청 없이 바로 이동
---

# <a> (하이퍼링크)

```sql
<a href="url"></a>
```

### 역할

- 다른 페이지로 이동
- GET 방식 요청
### 이미지 링크

```sql
<a href="https://www.naver.com/">
    <img src="notepad.png" width="100" height="100">
</a>
```

- 이미지를 클릭하면 이동
---

# <img> (이미지)

```sql
<img src="notepad.png" width="100px" height="100px">
```

- 이미지 표시
- src : 이미지 경로
- width / height : 크기
---

# 태그

### 수평선

```sql
<hr>
```

### 줄 바꿈

```sql
<br>-
```

---

# JSP 전용 태그

### 스크립틀릿 (자바 코드)

```sql
<%
String name = (String)request.getAttribute("name");
%>
```

- 서버에서 실행되는 자바 코드
- 클라이언트는 절대 못 봄
### 출력 표현식

```sql
<%= name %>
```

- 자바 변수 값을 HTML로 출력


