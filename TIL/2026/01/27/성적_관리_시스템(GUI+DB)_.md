# 성적 관리 시스템(GUI+DB) 

> 날짜: 2026-01-27
> 원본 노션: [링크](https://www.notion.so/GUI-DB-2f5b28703eb0803290d1ff05b12ee72b)

---

```java
package score;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
	private static DBConnection dbConn = new DBConnection();
	
	
	// 생성자 잠금
	private DBConnection() { // 생성자
		
	}
	
	// 위에서 생성한 인스턴스 얻기
	public static DBConnection getInstance() {
		return dbConn;
	}

	// 접속정보 주는 getConn()메소드 만들기
	public Connection getConn() {
		Connection conn = null;
		try {
			Class.forName("org.mariadb.jdbc.Driver");
			String url = "jdbc:mariadb://db.wisejia.com:3306/dswu04";
			String id = "dswu04";
			String passwd = "ck319gh";
			conn = DriverManager.getConnection(url, id, passwd);
		} catch (ClassNotFoundException e) {
			System.out.println("드라이버 클래스가 없습니다.");
			e.printStackTrace();
		} catch (SQLException e) {
			System.out.println("접속정보를 다시 확인해주세요.");
			e.printStackTrace();
		}
		return conn;
	}
}

```

```java
package score;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import score.ScoreDTO;
import score.DBConnection;

public class ScoreDAO {
	// 앞에서 생성한 싱글턴 패턴 연결해서 사용하기;
	
		// 수정하기 
		public int update(ScoreDTO dto) {
			int result = 0;
			String sql = "UPDATE score SET name = ?, kor = ?, eng = ?, mat = ?, tot = ?, ave = ?  WHERE no = ? ";
			
			try (Connection conn = DBConnection.getInstance().getConn();
				 PreparedStatement pstmt = conn.prepareStatement(sql);) {
				//sql의 ?자리 세팅 
				pstmt.setString(1, dto.getName()); 
				pstmt.setInt(2, dto.getKor()); 
				pstmt.setInt(3, dto.getEng()); 
				pstmt.setInt(4, dto.getMat()); 
				pstmt.setInt(5, dto.getTot());
				pstmt.setInt(6, dto.getAve()); 
				pstmt.setInt(7, dto.getNo()); 
				result = pstmt.executeUpdate();
			} catch (Exception e) {
				System.out.println("수정 중에 문제 발생");
			}
			return result;
		}
		
		//추가 
		public int insert(ScoreDTO dto) {
			int result = 0;
			String sql = "INSERT INTO score (NAME, kor, eng, mat, tot, ave) VALUES (?,?,?,?,?,? )";
			
			try (Connection conn = DBConnection.getInstance().getConn();
				 PreparedStatement pstmt = conn.prepareStatement(sql);) {
				//sql의 ?자리 세팅 
				pstmt.setString(1, dto.getName());
				pstmt.setInt(2, dto.getKor()); 
				pstmt.setInt(3, dto.getEng());
				pstmt.setInt(4, dto.getMat());
				pstmt.setInt(5, dto.getTot());
				pstmt.setInt(6, dto.getAve());
				result = pstmt.executeUpdate();
			} catch (Exception e) {
				System.out.println("삽입 중에 문제 발생");
			}
			return result;
		}
		
		// 삭제하기 delete(23);
		public int delete(int no) {
			int number = 0;
			String sql = "DELETE FROM score WHERE no=?";
			
			try (Connection conn = DBConnection.getInstance().getConn();
				 PreparedStatement pstmt = conn.prepareStatement(sql);) {
				//sql의 ?자리 세팅 
				pstmt.setInt(1, no); //첫번째 자리에 no가 들어간다는 의미 
				number = pstmt.executeUpdate();
				
			} catch (Exception e) {
				System.out.println("삭제 중에 문제 발생");
			}
			
			return number;
		}
		
		// 불러오기 
		public Vector select() {
			Vector<Vector<Object>> data = new Vector<>();
			String sql = "SELECT * FROM score";

			try (Connection conn = DBConnection.getInstance().getConn();
					PreparedStatement pstmt = conn.prepareStatement(sql);
					ResultSet rs = pstmt.executeQuery();) {

				while (rs.next()) {
		            Vector<Object> row = new Vector<>();
		            row.add(rs.getString("no"));
		            row.add(rs.getString("name"));
		            row.add(rs.getInt("kor"));
		            row.add(rs.getInt("eng"));
		            row.add(rs.getInt("mat"));
		            row.add(rs.getInt("tot"));
		            row.add(rs.getInt("ave"));
		            data.add(row);
		        }
			} catch (SQLException e) {
				e.printStackTrace();
			}

			return data;
		}
	}


```

```java
package score;
import java.time.LocalDateTime;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ScoreDTO {
	private String name;
	private int kor, eng, mat, tot, ave, no;
}

```

```java
package score;

import java.awt.event.*;
import java.util.*;
import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;

import score.ScoreDAO;
import score.ScoreDTO;

import java.awt.Dimension;
import java.awt.Font;
import java.awt.Toolkit;

class ScoreFrame extends JFrame implements ActionListener, MouseListener {
	
	JLabel jlNo, jlName, jlKor, jlEng, jlMat;
	JTextField jtNo, jtName, jtKor, jtEng, jtMat;
	JButton jbAdd, jbDel, jbChange;
	JTable table;
	Vector<String> data, col;
	
	ScoreDAO dao;
	ScoreDTO dto;
	
	ScoreFrame() {
		setLayout(null);
		dao = new ScoreDAO();
		dto = new ScoreDTO();

		
		//no
		add(jlNo = new JLabel("no", JLabel.CENTER));
		jlNo.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jlNo.setBorder(BorderFactory.createBevelBorder(0));
		jlNo.setBounds(10, 10, 120, 50);
		add(jtNo = new JTextField());
		jtNo.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jtNo.setHorizontalAlignment(JTextField.CENTER);
		jtNo.setBounds(140, 10, 120, 50);
		
		// 이름 
		add(jlName = new JLabel("이름", JLabel.CENTER));
		jlName.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jlName.setBorder(BorderFactory.createBevelBorder(0));
		jlName.setBounds(10, 70, 120, 50);
		add(jtName = new JTextField());
		jtName.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jtName.setHorizontalAlignment(JTextField.CENTER);
		jtName.setBounds(140, 70, 120, 50);
		
		// 국어
		add(jlKor = new JLabel("국어 점수", JLabel.CENTER));
		jlKor.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jlKor.setBorder(BorderFactory.createBevelBorder(0));
		jlKor.setBounds(10, 130, 120, 50);
		add(jtKor = new JTextField());
		jtKor.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jtKor.setHorizontalAlignment(JTextField.CENTER);
		jtKor.setBounds(140, 130, 120, 50);
		
		// 영어
		add(jlEng = new JLabel("영어 점수", JLabel.CENTER));
		jlEng.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jlEng.setBorder(BorderFactory.createBevelBorder(0));
		jlEng.setBounds(10, 190, 120, 50);
		add(jtEng = new JTextField());
		jtEng.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jtEng.setHorizontalAlignment(JTextField.CENTER);
		jtEng.setBounds(140, 190, 120, 50);
		
		// 수학
		add(jlMat = new JLabel("수학 점수", JLabel.CENTER));
		jlMat.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jlMat.setBorder(BorderFactory.createBevelBorder(0));
		jlMat.setBounds(10, 250, 120, 50);
		add(jtMat = new JTextField());
		jtMat.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jtMat.setHorizontalAlignment(JTextField.CENTER);
		jtMat.setBounds(140, 250, 120, 50);
		
		
		// 버튼
		add(jbAdd = new JButton("추가"));
		jbAdd.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jbAdd.setBounds(270, 10, 120, 50);
		jbAdd.addActionListener(this);
		add(jbDel = new JButton("제거"));
		jbDel.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jbDel.setBounds(270, 70, 120, 50);
		jbDel.addActionListener(this);
		add(jbChange = new JButton("수정"));
		jbChange.setFont(new Font("맑은 고딕", Font.BOLD, 20));
		jbChange.setBounds(270, 130, 120, 50);
		jbChange.addActionListener(this);
		
		// 컬럼 백터
		col = new Vector<>();
		col.add("no");
		col.add("이름");
		col.add("국어 점수");
		col.add("영어 점수");
		col.add("수학 점수");
		col.add("총점");
		col.add("평균");
		
		// 테이블 수정 못하게 DefaultTableModel 사용
		DefaultTableModel model = new DefaultTableModel(dao.select(), col) {
		    @Override
		    public boolean isCellEditable(int row, int column) {
		        return false;
		    }
		};
	
		
		/* 디폴트테이블을 테이블에 더해서 스크롤패널에 더한다 */
		table = new JTable(model);
		table.addMouseListener(this);
		JScrollPane scroll = new JScrollPane(table);
		jTableSet();
		add(scroll);
		scroll.setBounds(415, 10, 770, 250);
		
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		setLocation((screenSize.width - 1200) / 2, (screenSize.height - 300) / 2);
		
		setResizable(false);
		setSize(1200, 350);
		setTitle("성적 관리프로그램");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setVisible(true);

	}

	private void jTableSet() {
		// 이동과 길이조절 여러개 선택 되는 것을 방지한다
		table.getTableHeader().setReorderingAllowed(false);
		table.getTableHeader().setResizingAllowed(false);
		table.setSelectionMode(ListSelectionModel.SINGLE_INTERVAL_SELECTION);
		
		// 컬럼 정렬에 필요한 메서드
		DefaultTableCellRenderer celAlignCenter = new DefaultTableCellRenderer();
		celAlignCenter.setHorizontalAlignment(JLabel.CENTER);
		DefaultTableCellRenderer celAlignRight = new DefaultTableCellRenderer();
		celAlignRight.setHorizontalAlignment(JLabel.RIGHT);
		DefaultTableCellRenderer celAlignLeft = new DefaultTableCellRenderer();
		celAlignLeft.setHorizontalAlignment(JLabel.LEFT);
		
		// 컬럼별 사이즈 조절 & 정렬
		table.getColumnModel().getColumn(0).setPreferredWidth(10);
		table.getColumnModel().getColumn(0).setCellRenderer(celAlignCenter);
		table.getColumnModel().getColumn(1).setPreferredWidth(10);
		table.getColumnModel().getColumn(1).setCellRenderer(celAlignCenter);
		table.getColumnModel().getColumn(2).setPreferredWidth(10);
		table.getColumnModel().getColumn(2).setCellRenderer(celAlignCenter);
		table.getColumnModel().getColumn(3).setPreferredWidth(10);
		table.getColumnModel().getColumn(3).setCellRenderer(celAlignCenter);
		table.getColumnModel().getColumn(4).setPreferredWidth(20);
		table.getColumnModel().getColumn(4).setCellRenderer(celAlignCenter);
		table.getColumnModel().getColumn(5).setPreferredWidth(20);
		table.getColumnModel().getColumn(5).setCellRenderer(celAlignCenter);	
	}

	@Override
	public void mouseClicked(MouseEvent e) {
		int rowIndex = table.getSelectedRow();
		jtNo.setText(table.getValueAt(rowIndex, 0) + "");
		jtName.setText(table.getValueAt(rowIndex, 1) + "");
		jtKor.setText(table.getValueAt(rowIndex, 2) + "");
		jtEng.setText(table.getValueAt(rowIndex, 3) + "");
		jtMat.setText(table.getValueAt(rowIndex, 4) + "");
		
	}

	@Override
	public void mousePressed(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String ButtonFlag = e.getActionCommand();
//		Score test = new Score();
		
		if (ButtonFlag.equals("추가")) {
			try {
				int result = dao.insert(contentSet());
				if (result == 1) {
					JOptionPane.showMessageDialog(this, "추가 되었습니다.");
					jTableRefresh();
					contentClear();
				}
			} catch (Exception e2) {
				JOptionPane.showMessageDialog(this, "이름을 입력하세요!");
				e2.printStackTrace();
				return;
			}
		} else if (ButtonFlag.equals("제거")) {
			int result = 0;
			try {
				if (!jtNo.getText().equals("")) {
					result = dao.delete(Integer.parseInt(jtNo.getText()));
				}

				if (result == 1) {
					JOptionPane.showMessageDialog(this, "제거 되었습니다.");
					jTableRefresh();
					contentClear();
				} // inner if
			} catch (Exception e2) {
				JOptionPane.showMessageDialog(this, "no를 입력하세요!");
				e2.printStackTrace();
			} 
		} else if (ButtonFlag.equals("수정")) {
			int result=0;
			try {
				if (!jtNo.getText().equals("")) {
					ScoreDTO udto = contentSet();
					udto.setNo(Integer.parseInt(jtNo.getText()));
					result = dao.update(udto);
				}else {
					JOptionPane.showMessageDialog(this, "no를 입력하세요");
				}
				
				if (result == 1) {
					JOptionPane.showMessageDialog(this, "수정 되었습니다.");
					jTableRefresh();
					contentClear();				
					jtName.setFocusable(true);
				} // inner if
			} catch (Exception e2) {
				JOptionPane.showMessageDialog(this, "이름을 입력하세요!");
				e2.printStackTrace();
			} 
		}
	}

	private void jTableRefresh() {
		// 테이블 수정 못하게 DefaultTableModel 사용
		DefaultTableModel model = new DefaultTableModel(dao.select(), col) {
			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		table.setModel(model);
		jTableSet();
		
	}

	private void contentClear() {
		jtNo.setText("");
		jtName.setText("");
		jtKor.setText("");
		jtEng.setText("");
		jtMat.setText("");
	}


	private ScoreDTO contentSet() {
		ScoreDTO dto = new ScoreDTO();
		
		int kor, eng, mat, tot, ave;
		String name;

		name = jtName.getText();
	
		if(jtKor.getText().equals("")) {
			kor = 0;
		} else {
			kor = Integer.parseInt(jtKor.getText());
		}
		
		if(jtEng.getText().equals("")) {
			eng = 0;
		} else {
			eng = Integer.parseInt(jtEng.getText());
		}
		
		if(jtMat.getText().equals("")) {
			mat = 0;
		} else {
			mat = Integer.parseInt(jtMat.getText());
		}
		
		tot = kor + eng + mat; 
		ave = tot/3;
		
		dto.setName(name);
		dto.setKor(kor);
		dto.setEng(eng);
		dto.setMat(mat);
		dto.setTot(tot);
		dto.setAve(ave);	
		
		return dto;
		
	}
}

public class Score{

	public static void main(String[] args) {
		new ScoreFrame();
	}
}

```

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/cb3b2870-3eb0-815c-99e6-0003045e9130/d2b9ddca-1539-4018-8971-b8795ce84726/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YIAOVM4U%2F20260128%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260128T004723Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCThHv%2FibPh78%2BUnKlH3o4mWPBxuDBJJkOQXroeiiB2MAIhAN6uU1TsUDV%2FyZm2WAeodqscKXA5JKhrKH9uB7%2Fzf4EUKv8DCGEQABoMNjM3NDIzMTgzODA1IgzDxfklDQMyiJgvmWkq3ANx273xwBz0bK%2B%2BGMgFv33Rf3Lq22zzbLW%2Bn8nAMmngIMZK%2FxlNTqKP7YXwK%2FnS6cmms0rGMWguEWcx1LEqlHOfTYKeBuK70dR%2B2HtbmxtFL5FoJvMQ33yjZOCrxTEFeBn%2B3RzytIsSZCJUhV2YHnXXQiCayHPvUEtuzqXwo1H%2BhlRjrxT%2Bz2G1afhRWPNTvYSUAm21r9UB93T4QnfUqGJ5UI%2FVS%2BKocDlmlC1nJhNur2SWFZWEucd5EYy%2F%2BNuw49Is0uhBzsApdzwHtwugItjSlhL1DUsNo01lEotOEhKa4Mg3ELHWQUtqs7NJxP%2Bk7ZWSAy1CBjlRaSVotdHW26zAN3JEWTASrFFGFDd3%2FORzfd0jwjyJr81L6LTMaeSAnu5d2h%2FvVWv6SA%2Fb1V3ooIKvKeuxs%2B3k%2FBHzOuKDBdSmbOSI3n%2FFfLKaz7L7lTecPUDYf%2BWLMq0LcKTNCp5abLAtnh0d4bSTVFlS47XhmeLYI1PaHozhrta3%2FVKtQoVT5y5ZBHLiw8rrEzw%2BgggpoKnOO4njF1lM1mvSJ6CkB4zg8GrulLIhTmezAI0IDQIIBmF1MYmQo3Du4JAwzRVtwKSYsBVvYul3Y6xgqjjxBOZiHQTEF9D%2BAk8F3Wnl5zD5mOXLBjqkAeN1lBEXjYuDHpl1N4MUd1jvdJYbOOnI0dH8LimecGIzsH0ovawCYECe3aL0AShBZiZqTt002jAw8nQbIR%2FLZ1JgwJHT%2FEihZcNCV1n7SSylLWV8xiTSiO68c9AFx3YXIn1oRiQ5L87s9AxSEYGgIrdeABUip38NR5aWfRdwv%2BS4%2B7A1QHzrm1be4w3KiSz9dWY29OYj35AIX5m19rpEgzZ94eEN&X-Amz-Signature=cc3cf15560de0304395fe586d5656ccb9bd756a28f874295e98ff8aa30898dba&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

기본키 : no 

추가 - 이름, 국어점수, 영어점수, 수학점수를 입력하면 추가 

제거 - no를 입력하면 해당 no행 삭제 

수정 - no, 이름, 국어점수, 영어점수, 수학점수를 입력하면 수정



