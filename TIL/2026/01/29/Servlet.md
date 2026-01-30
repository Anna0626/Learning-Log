# Servlet

> 날짜: 2026-01-29
> 원본 노션: [링크](https://www.notion.so/Servlet-2f7b28703eb080c091b2c645d0524c5c)

---

# 서블릿 

### 표준 http 상태 코드 

- 100 : 정보 전달 
- 200 성공 
- 300 : 리다이렉션 
- 400 / 404 : 페이지 없음
- 500 / 505 : 서버 오류(서버의 로직에 문제가 생겼을 때)
---

### 파라미터 값 가져오기 

자바 서블릿(JSP)에서 클라이언트(브라우저)가 보낸 요청 파라미터 값을 가져오는 메서드

```sql
request.getParameter("파라미터명");
```

### 서버에서 JSP로 데이터 전달

request 객체에 name이라는 데이터를 담는다

이 데이터는 forward 되는 동안만 유지

### 이동할 JSP를 지정+데이터 전달

이동할 JSP를 지정

```sql
RequestDispatcher rd = request.getRequestDispatcher("/login.jsp"); 
```

/login.jsp 로 요청을 넘길 준비, 이동X

이동 + 데이터 전달

```sql
rd.forward(request, response);
```

- URL은 안 바뀜
- equest 객체 그대로 JSP로 전달됨
- setAttribute 한 값도 같이 감
JSP에서 값 받기



