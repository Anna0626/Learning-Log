# CRUD

> 날짜: 2026-01-26
> 원본 노션: [링크](https://www.notion.so/CRUD-2f4b28703eb080579ad0f26270b1c502)

---

# CREATE 

데이터 입력하기 

```javascript
	public int insert(BoardDTO dto) {
		int result = 0;
		String sql = "INSERT INTO board (board_title, board_writer) VALUES (?,?)";
		
		try (Connection conn = DBConnection.getInstance().getConn();
			 PreparedStatement pstmt = conn.prepareStatement(sql);) {
			//sql의 ?자리 세팅 
			pstmt.setString(1, dto.getBoard_title()); //첫번째 자리에 title가 들어간다 
			pstmt.setString(2, dto.getBoard_writer()); //두번째 자리에 writer가 들어간다 
			result = pstmt.executeUpdate();
		} catch (Exception e) {
			System.out.println("삽입 중에 문제 발생");
		}
		return result;
	}
```

# READ 

데이터 불러오기 

```javascript
	public List<BoardDTO> select() {
		List<BoardDTO> list = new ArrayList<BoardDTO>();
		String sql = "SELECT * FROM board";

		try (Connection conn = DBConnection.getInstance().getConn();
				PreparedStatement pstmt = conn.prepareStatement(sql);
				ResultSet rs = pstmt.executeQuery();) {

			while (rs.next()) {
				BoardDTO dto = new BoardDTO();
				dto.setBoard_no(rs.getInt("board_no"));
				dto.setBoard_title(rs.getString("board_title"));
				dto.setBoard_writer(rs.getString("board_writer"));
				dto.setBoard_date(rs.getObject("board_date", LocalDateTime.class));
				dto.setBoard_read(rs.getInt("board_read"));
				list.add(dto);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
```

# UPDATE 

데이터 수정하기 

```javascript
	public int update(BoardDTO dto) {
		int result = 0;
		String sql = "UPDATE board SET board_title = ?,  board_writer = ? WHERE board_no = ? ";
		
		try (Connection conn = DBConnection.getInstance().getConn();
			 PreparedStatement pstmt = conn.prepareStatement(sql);) {
			//sql의 ?자리 세팅 
			pstmt.setString(1, dto.getBoard_title()); //첫번째 자리에 title가 들어간다는 의미 
			pstmt.setString(2, dto.getBoard_writer()); //두번째 자리에 writer가 들어간다는 의미 
			pstmt.setInt(3, dto.getBoard_no()); //두번째 자리에 writer가 들어간다는 의미 
			result = pstmt.executeUpdate();
		} catch (Exception e) {
			System.out.println("수정 중에 문제 발생");
		}
		return result;
	}
```

# DELETE 

데이터 수정하기 

```javascript
	public boolean delete(int no) {
		boolean result = false;
		String sql = "DELETE FROM board WHERE board_no=?";
		
		try (Connection conn = DBConnection.getInstance().getConn();
			 PreparedStatement pstmt = conn.prepareStatement(sql);) {
			//sql의 ?자리 세팅 
			pstmt.setInt(1, no); //첫번째 자리에 no가 들어간다는 의미 
			int number = pstmt.executeUpdate();
			
			if(number == 1) {
				result = true;
			}
		} catch (Exception e) {
			System.out.println("삭제 중에 문제 발생");
		}
		
		return result;
	}
```



### 예시

```javascript
package db;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.List;
import java.util.Scanner;

public class Test {
	static String str1;
	static String str2;
	public static void main(String[] args) {
		
		//데이터 불러오기
		BoardDAO dao = new BoardDAO();
		List<BoardDTO> list = dao.select();
		//System.out.println(list); // db.BoardDTO@604ed9f0 
		
		//스캐너 
		Scanner sc = new Scanner(System.in);
		
		// Test 인스턴스 생성
		Test test = new Test();
		
		boolean exit = true;
		while (exit) { 
			System.out.print("1.출력 2.추가 3.삭제 4.수정 5.종료 > ");
			int num = sc.nextInt();
			sc.nextLine();
			switch(num) {
			case 1:
				test.print(dao.select());
				break;
			case 2:
				dao.insert(test.insert(sc));
				break;
			case 3:
				dao.delete(test.del(sc));
				break;
			case 4:
				dao.update(test.update(sc));
				break;
			case 5:
				exit = !exit;
				break;
			default: 
				System.out.println("다시 입력해주세요");
				break;
			}
		}
		System.out.println("종료되었습니다. ");
		
		//닫기 
		sc.close();
	}

	public BoardDTO update(Scanner sc) {
		System.out.print("수정할 번호를 입력하세요 : ");
		int no = sc.nextInt();
		sc.nextLine();
		BoardDTO dto = insert(sc);
		dto.setBoard_no(no);
		return dto;
	}
	
	public int del(Scanner sc) {
		System.out.print("삭제할 번호:");
		int num = sc.nextInt();
		
		return num;
	}
	
	public BoardDTO insert(Scanner sc) {
		BoardDTO dto = new BoardDTO();
		System.out.print("제목을 입력하세요 : ");
		dto.setBoard_title(sc.nextLine());
		System.out.print("글쓴이를 입력하세요 : ");
		dto.setBoard_writer(sc.nextLine());
		return dto;
	}
	
	public void print(List<BoardDTO> list) {
		System.out.println("번호\t제목\t글쓴이\t쓴날짜\t읽음수");
		for(BoardDTO dto : list) {
			System.out.printf("%d\t%s\t%s\t%s\t%d\n", dto.getBoard_no(), 
					dto.getBoard_title(), dto.getBoard_writer(), dto.getBoard_date(), dto.getBoard_read());
		}
	}
}
```

