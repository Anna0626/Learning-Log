# DAO 패턴 기반 데이터베이스 CRUD

> 날짜: 2026-01-20
> 원본 노션: [링크](https://www.notion.so/DAO-CRUD-2eeb28703eb08088a1b7f2b2c61c2944)

---

CRUD(Database CRUD Operations)


| 화면 출력 | 데이터 입력 | 데이터 수정 | 데이터 삭제 |
| --- | --- | --- | --- |
| select | insert | update | delete |


| execute() | return 값: resultset/true/false |
| --- | --- |
| executeUpdate() | insert, update, delete의 return 값: 영향 받은 행의 수(int형) |
| executeQuery() | select문 실행할 때 사용, return 값: ResultSet |

 1. jar 연결 

2. DBConnection 가져오기 

3. DTO 가져오기 

4. DAO 생성

## DBTest

```javascript
package db;
import java.util.*;

public class DBTest {
	public static void main(String[] args) {
		BoardDAO dao = new BoardDAO();
		List<BoardDTO> list = dao.select();
		Scanner sc = new Scanner(System.in);
		int num;
		boolean exit = true;
		
		while(exit) {
			System.out.print("(1)print (2)write (3)delete (4)exit : ");
			num = sc.nextInt();
			sc.nextLine();   //남아있는 엔터 제거
			
			switch(num) {
			case 1: 
				print(dao.select()); break;
			case 2: 
				write(sc, dao); break;
			case 3: 
				delete(sc, dao); break;
			case 4:
				exit = !exit; break;
			}
		}
		sc.close();
	}
	
	private static void delete(Scanner sc, BoardDAO dao) {
		System.out.print("삭제할 번호를 입력하세요 : ");
		int num = sc.nextInt();
		int result = dao.delete(num);
		System.out.println(result + "개 삭제되었습니다. ");
	}
	
	//글 저장하기 메소드 
	private static void write(Scanner sc, BoardDAO dao) {
		//스캐너 생성 
		//제목 / 글쓴이 / 내용 -> 입력 받아서 DTO로 넣는다.
		System.out.print("제목 입력 : ");
		String title = sc.nextLine();			//단어 : 공백 전까지 읽기 : 공백/엔터를 버퍼에 남김
		System.out.print("글쓴이 입력 : ");
		String writer = sc.nextLine();
//		sc.nextLine();						//엔터키 처리
		System.out.print("본문 입력 : ");
		String content = sc.nextLine();		//한 줄 : 엔터 전까지 읽기 : 버퍼에서 제거  
		
		BoardDTO dto = new BoardDTO();
		dto.setTitle(title);
		dto.setWriter(writer);
		dto.setContent(content);
		
		int result = dao.insert(dto);
	}
	
	//print
	   private static void print(List<BoardDTO> list) {
	      System.out.println("번호\t제목\t\t글쓴이\t날짜\t\t\t읽음");
	      for (BoardDTO dto : list) {
	         System.out.print(dto.getNo()+"\t");
	         System.out.printf("%-10s\t",dto.getTitle());
	         System.out.print(dto.getWriter()+"\t");
	         System.out.print(dto.getDate()+"\t");
	         System.out.print(dto.getRead()+"\n");
	      }
	   }
}
```

## DBConnection

데이터베이스 접속 정보

```javascript
package db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
	//접속정보를 내보내는 메소드, DAO가 사용
	public Connection getConnection() {
		Connection conn = null; // 접속 정보 저장할 객체
		String url = "jdbc:mariadb://db.wisejia.com:3306/dswu04"; // URL:PORT/DBname
		String id = "dswu04";  //개인 ID, DB명과 ID가 같음 
		String passwd = "ck319gh"; // 차319호

		// class 가져오기
		try {
			Class.forName("org.mariadb.jdbc.Driver"); // 패키지명.클래스명
			// 조립
			conn = DriverManager.getConnection(url, id, passwd);
		} catch (ClassNotFoundException e) {
			System.err.println("드라이버 클래스가 없습니다.");
		} catch (SQLException e) {
			System.err.println("접속 정보에 문제가 있습니다. 확인해주세요.");
		}
		return conn;
	}
}

```

## BoardDAO

CRUD R

```javascript
package db;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class BoardDAO {
	// CRUD R
	public List<BoardDTO> select() {
		List<BoardDTO> list = new ArrayList<BoardDTO>();
		
		String sql = "SELECT t.no, t.title, t.writer, t.date, t.read FROM testboard t";
		
		//이런식으로 하면 블록을 나가면 자동으로 close()가 된다. 불필요한 리소스들을 닫아준다. 
		try (Connection conn = new DBConnection().getConnection();
				PreparedStatement pstmt = conn.prepareStatement(sql);
				ResultSet rs = pstmt.executeQuery();) {

			while (rs.next()) {
				BoardDTO dto = new BoardDTO();
				dto.setNo(rs.getInt("no"));
				dto.setTitle(rs.getString("title"));
				dto.setDate(rs.getString("date"));
				dto.setWriter(rs.getString("writer"));
				dto.setRead(rs.getInt("read"));
				list.add(dto);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}

		return list;
	}

	public int insert(BoardDTO dto) {
		int result = 0;   // 1은 성공 : 영향받은 행의 수  
		
		//저장에 필요한 sql문 
		String sql ="INSERT INTO testboard (title, writer, content) VALUES (?, ?, ?)";
		
		try(Connection conn = new DBConnection().getConnection();
				PreparedStatement pstmt = conn.prepareStatement(sql);){
			pstmt.setString(1, dto.getTitle());
			pstmt.setString(2, dto.getWriter());
			pstmt.setString(3, dto.getContent());
			result = pstmt.executeUpdate();		//실제 데이터베이스에 쓰기 동작
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return result;
	}
	
	public int delete(int num) {
		int result = 0;
		String sql = "DELETE FROM testboard WHERE no=?";
		
		try (Connection conn = new DBConnection().getConnection();
		PreparedStatement pstmt = conn.prepareStatement(sql);){
			//위치 세팅
			pstmt.setInt(1, num);
			//실행 
			result = pstmt.executeUpdate();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return result;   //0: 실패(no컬럼에 없는 번호이거나 삭제 오류) 1: 성공
	}
}

```

## BoardDTO

데이터를 계층간 전달하기 위한 객체

```javascript
package db;

public class BoardDTO {
	// 값 저장하는 필드
	private int no, read;
	private String title, writer, date, content;
	
	// 값 가공하는 메소드 //setter getter --> 롬복(Lombok) 사용하면 편리함
	public int getNo() {
		return no;
	}

	public void setNo(int no) {
		this.no = no;
	}

	public int getRead() {
		return read;
	}

	public void setRead(int read) {
		this.read = read;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getWriter() {
		return writer;
	}

	public void setWriter(String writer) {
		this.writer = writer;
	}

	public String getDate() {
		return date;
	}

	public void setDate(String date) {
		this.date = date;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}
}
```

