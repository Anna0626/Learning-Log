# web

> 날짜: 2026-01-26
> 원본 노션: [링크](https://www.notion.so/web-2f4b28703eb08084a03ecad3638fecbc)

---

# 생성

File → new → Other… → Web → Dynamic Web Project 

Target runtime : New Runtime.. → Apache → Apache Tomcat v10.1



java code file : Java Resources/src/main/java

html file : src/main

---

# Servlet

줄 바꿈 : pw.print("<br>");

구분 선 : pw.println("<hr>");

## doGet 메소드

Get방식에서 호출되는 메소드. 데이터가 URL에 포함된다.

```javascript
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
}
```

- form 태그 내 method 속성을 입력하지 않으면 기본값인 'get 방식'으로 요청하게 된다.
## doPost 메소드 

Post방식에서 호출되는 메서드. 데이터가 HTML header에 포함된다.

```javascript
protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
}
```

### 예시

```javascript
package web;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import db.BoardDAO;
import db.BoardDTO;

@WebServlet("/board")
public class Board extends HttpServlet {
	private static final long serialVersionUID = 1L;
    public Board() {
        super();
    }
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setCharacterEncoding("UTF-8");
		response.setContentType("text/html; charset=UTF-8");
		//문장 단위로 읽어들이기 PrintWriter
		PrintWriter pw = response.getWriter();
		pw.println("출력");
		pw.println("<hr>");  //구분선 긋기
		// 데이터베이스의 값 출력 
		BoardDAO dao = new BoardDAO();
		List<BoardDTO> list = dao.select();
		for (BoardDTO dto : list) {
			pw.print(dto.getBoard_no() + "/");
			pw.print(dto.getBoard_title() + "/");
			pw.print(dto.getBoard_writer() + "/");
			pw.print(dto.getBoard_date() + "/");
			pw.print(dto.getBoard_read());
			pw.print("<br>");
		}
		pw.println("<br>");
	}
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}

```



