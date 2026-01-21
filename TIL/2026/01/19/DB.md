# DB

> 날짜: 2026-01-19
> 원본 노션: [링크](https://www.notion.so/DB-2edb28703eb080ccb0bcd10152203978)

---

# DTO

전송 객체 Data Transfer Object

- 데이터를 계층 간 전달하기 위한 객체 
- 택배 상자
- 비슷한 객체로는 VO(Value Object) : 값 자체를 표현하는 객체, 읽기만 가능
- Entity 
---

# DAO

접속 객체 Database Access Object 

- 데이터베이스에 접속하는 객체
- SQL 명령어 실행, DTO에 저장

| CURD 작업 | Create | Read | Update | Delete |
| --- | --- | --- | --- | --- |
| 데이터베이스 | INSERT | SELECT | UPDATE | DELETE |
| Rest API | post | get | put/patch | delete |

- 사용 목적
---

# mariaDB를 활용한 데이터베이스 가져오기

### DBConnection

### BoardDAO

### BoardDTO

### DBTest

출력 결과: 

```javascript
번호	제목		        글쓴이	    날짜			             읽음
1	    접속성공      	  홍길동	    2026-01-14 18:05:27	   1
2	    집에가고싶어요   	테스터	    2026-01-14 17:53:01	   1
```



