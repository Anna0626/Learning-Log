# Socket

> 날짜: 2026-01-28
> 원본 노션: [링크](https://www.notion.so/Socket-2f6b28703eb080289548e8c8c29215c3)

---

client 

```java
package net;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

public class Client {
	public static void main(String[] args) {
		Scanner sc = null;
		Socket so = null;
		
		try {
			sc = new Scanner(System.in);
			so = new Socket("localhost", 5001);
			
			//출력작업
			OutputStream os = so.getOutputStream();
			OutputStreamWriter osw = new OutputStreamWriter(os);
			BufferedWriter bw = new BufferedWriter(osw);
			
			String txt = "";
			
			while (true) {
				System.out.print("내용 : ");
				txt = sc.nextLine();
				bw.write(txt + "\n"); //=\n을 붙여야 서버로 날아갑니다.
				bw.flush();//강제전송
			}
			
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if(so != null) {
				try {
					so.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			if(sc != null) {
				sc.close();
			}
		}
	}
}
```

```java
package net;

import java.awt.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

import javax.swing.*;

public class Client02 implements ActionListener, Runnable {

	private Socket socket;
	private ObjectInputStream ois;
	private ObjectOutputStream oos;
	private JFrame jframe; // 윈도우 창
	private JTextField jtf; // 채팅 입력란
	private JTextArea jta; // 채팅 내용 보여주는 객체
	private JLabel jlb1, jlb2; // 라벨
	private JPanel jp1, jp2; // 판넬
	private String ip; // IP 주소를 저장할 변수
	private String id; // 닉네임 저장할 변수
	private JButton jbtn; // 종료버튼

	public Client02(String argIp, String argId) {
      ip = "localhost";
      id = argId;
      jframe = new JFrame("멀티 채팅 ver 1.0");
      //아래에 붙는 코드
      jp1 = new JPanel();
      jp1.setLayout(new BorderLayout());
      jtf = new JTextField(30); // 30문자
      jbtn = new JButton("종료"); // 종료 버튼 생성
      jp1.add(jbtn, BorderLayout.EAST);
      jp1.add(jtf, BorderLayout.CENTER);
      //위쪽에 붙이는 판넬 코드
      jp2 = new JPanel(); // 위쪽에 붙는 판넬
      jp2.setLayout(new BorderLayout());
      jlb1 = new JLabel("대화명 : [[" + id + "]]"); // IP주소 : 127.0.0.1
      jlb1.setBackground(Color.YELLOW);
      jlb2 = new JLabel("IP 주소 : " + ip); // IP주소 : 127.0.0.1
      jlb2.setBackground(Color.GREEN);
      jp2.add(jlb1, BorderLayout.CENTER);
      jp2.add(jlb2, BorderLayout.EAST);
      // 프레임에 붙이는 코드
      jta = new JTextArea("", 10, 50);
      jta.setBackground(Color.ORANGE);
      JScrollPane jsp = new JScrollPane(jta,
         JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
         JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
      jframe.add(jp1, BorderLayout.SOUTH);
      jframe.add(jp2, BorderLayout.NORTH);
      jframe.add(jsp, BorderLayout.CENTER);
      // 감지기 붙이는 코드
      jtf.addActionListener(this);
      jbtn.addActionListener(this);
      //x클릭시 처리하는 코드 등 정의
      jframe.addWindowListener(new WindowAdapter() {

         @Override
         public void windowClosing(WindowEvent e) {
            try{
               oos.writeObject(id + "#exit");
            }catch(Exception ee) {
               ee.printStackTrace();
            }
            System.exit(0); // 프로그램종료
         } //
         @Override
         public void windowOpened(WindowEvent e) { // 이벤트 처리
            jtf.requestFocus(); // jtf에 포커스를 놓는다.
         }         
      }); // 윈도우 이벤트 처리 끝
      jta.setEditable(false); // 편집 X , 채팅 내용 보여주기만 함
      jframe.pack(); // 자동 크기 지정
      jframe.setResizable(false); // 창 크기 변경 X
      jframe.setVisible(true); // 보이기
   } // 생성자

	@Override
	public void actionPerformed(ActionEvent e) {
		Object obj = e.getSource(); // 이벤트 발생 위치 열기
		String msg = jtf.getText(); // 채팅 내용 입력 받기
		if (obj == jtf) {
			if (msg == null || msg.length() == 0) {
				// 경고창
				JOptionPane.showMessageDialog(jframe, "글을 쓰세요", "경고", JOptionPane.WARNING_MESSAGE);
			} else { // 내용을 입력하고 엔터한 경우
				try {
					oos.writeObject(id + "#" + msg);
				} catch (Exception ee) {
					ee.printStackTrace();
				}
				jtf.setText(""); // jtf를 지운다.
			} // else : 내용 0
		} else if (obj == jbtn) { // 종료 버튼 클릭
			try {
				oos.writeObject(id + "#exit");
			} catch (Exception ee) {
				ee.printStackTrace();
			}
			System.exit(0);
		}
	}

	public void init() {
		try {
			socket = new Socket(ip, 5000);
			System.out.println("서버에 접속되었습니다... 주인님^^");
			oos = new ObjectOutputStream(socket.getOutputStream());
			ois = new ObjectInputStream(socket.getInputStream());
			Thread t = new Thread(this);
			t.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		JFrame.setDefaultLookAndFeelDecorated(true);
		Client02 cc = new Client02("ip", "사용자이름");
		cc.init();
	}

	@Override
	public void run() {
		String message = null;
		String[] receiveMsg = null;
		boolean isStop = false;
		while (!isStop) {
			try {
				message = (String) ois.readObject(); // 채팅내용
				receiveMsg = message.split("#");
			} catch (Exception e) {
				e.printStackTrace();
				isStop = true; // 반복문 종료로 설정
			}
			System.out.println(receiveMsg[0] + " : " + receiveMsg[1]);
			if (receiveMsg[1].equals("exit")) {
				if (receiveMsg[0].equals(id)) {
					System.exit(0);
				} else {
					jta.append(receiveMsg[0] + "님이 종료했습니다\n");
					// 커서를 현재 채팅 내용의 자리에 보여준다.
					jta.setCaretPosition(jta.getDocument().getLength());
				}
			} else {
				jta.append(receiveMsg[0] + " : " + receiveMsg[1] + "\n"); // 홍길 : 안녕
				// 커서를 현재 채팅 내용의 자리에 보여준다.
				jta.setCaretPosition(jta.getDocument().getLength());
			}
		}
	}

}

```

server

```java
package com.poseidon.chatting;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

	public static void main(String[] args) {
		ServerSocket serverSocket = null;
		try {
			System.out.println("서버실행 중");
			serverSocket = new ServerSocket(5001);
			Socket s = serverSocket.accept();
			System.out.println("접속 성공");

			InputStream is = s.getInputStream();
			InputStreamReader isr = new InputStreamReader(is);
			BufferedReader br = new BufferedReader(isr);

			while (true) {
				System.out.println(br.readLine());
			}

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if(serverSocket != null) {
				try {
					serverSocket.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}

}

```

```java
package net;

import java.awt.BorderLayout;
//  입출력이 일어난다.
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
//  네트워크 프로그램.
import java.net.ServerSocket;
import java.net.Socket;
//  ArrayList 사용(클라이언트를 담는 역할)
import java.util.ArrayList;

import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class Server02 extends JFrame {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private ArrayList<MultiServerThread> list;
	private Socket socket;
	JTextArea ta;
	JTextField tf;

	public Server02() {
		// 화면 디자인 코드
		setTitle("채팅 서버 ver 1.0");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		ta = new JTextArea();
		add(new JScrollPane(ta));
		tf = new JTextField();
		tf.setEditable(false);
		add(tf, BorderLayout.SOUTH);
		setSize(300, 300);
		setVisible(true);

		// 채팅 관련 코드
		list = new ArrayList<MultiServerThread>();
		try (ServerSocket serverSocket = new ServerSocket(5000)) {
			MultiServerThread mst = null;// 한 사용자 담당할 채팅 객체
			boolean isStop = false; // 깃발 값
			tf.setText("서버 정상 실행중입니다. 주인님^^\n");
			while (!isStop) {
				socket = serverSocket.accept();// 클라이언트별 소켓 생성
				mst = new MultiServerThread();// 채팅 객체 생성
				list.add(mst);// ArrayList에 채팅 객체 하나 담는다.
				mst.start();// 쓰레드 시작
			} // while
		} catch (IOException e) {
			e.printStackTrace();
		} // catch
	}// 생성자

	public static void main(String[] args) {
		new Server02();
	}// main

	// 내부 클래스
	class MultiServerThread extends Thread {
		private ObjectInputStream ois;
		private ObjectOutputStream oos;

		@Override
		public void run() {
			boolean isStop = false; // flag value(깃발 값)
			try {
				ois = new ObjectInputStream(socket.getInputStream());
				oos = new ObjectOutputStream(socket.getOutputStream());
				String message = null; // 채팅 내용을 저장할 변수
				while (!isStop) {
					message = (String) ois.readObject();// 클라이언트 입력 받기
					String[] str = message.split("#");// 홍길동#방가방가
					if (str[1].equals("exit")) { // 홍길동#exit, 종료하겠다는 뜻
						broadCasting(message);// 모든 사용자에게 내용 전달
						isStop = true; // 종료
					} else {
						broadCasting(message);// 모든 사용자에게 채팅 내용 전달
					} // else
				} // while
				list.remove(this);// 홍길동을 뺀다.
				ta.append(socket.getInetAddress() + " IP 주소의 사용자께서 종료하셨습니다.\n");
				tf.setText("남은 사용자 수 : " + list.size());
			} catch (Exception e) {
				list.remove(this);// 장길산을 뺀다.
				ta.append(socket.getInetAddress() + " IP 주소의 사용자께서 비정상 종료하셨습니다.");
				tf.setText("남은 사용자 수 : " + list.size());
			} // catch
		}// run

		public void broadCasting(String message) {// 모두에게 전송
			for (MultiServerThread ct : list) {
				ct.send(message);
			} // for
		}// broadCasting

		public void send(String message) { // 한 사용자에게 전송
			try {
				oos.writeObject(message);
			} catch (IOException e) {
				e.printStackTrace();
			} // catch
		}// send
	}// 내부 클래스

}// end

```

---

# NetStream

```java
package net;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class NetStream {
	public static void main(String[] args) {
		URL url = null;
		BufferedReader br = null;
		
		try {
			url = new URL("https://www.naver.com");
//			URLConnection conn = url.openConnection();
//			InputStream ins = conn.getInputStream();
//			InputStream ins = url.openStream();
			br = new BufferedReader(new InputStreamReader(url.openStream()));
			String line = "";
			while((line = br.readLine()) != null) {
				System.out.println(line);
			}
				
			
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			
		}

	}

}

```

---

## URL

```java
package net;

import java.net.URL;

public class URLTest {
	public static void main(String[] args) {
		// https://www.clien.net/service/board/news/19133651?od=T31&po=0&category=0&groupCd=
		try {
			URL url = new URL("https://www.clien.net/service/board/news/19133651?od=T31&po=0&category=0&groupCd=");
			System.out.println("url.getAuthority() : " + url.getAuthority());
			System.out.println("url.getContent() : " + url.getContent());
			System.out.println("url.getDefaultPort() : " + url.getDefaultPort());
			System.out.println("url.getFile()" + url.getFile());
			System.out.println("url.getHost() : "+url.getHost());
			System.out.println("url.getPath() : " + url.getPath());
			System.out.println("url.getProtocol() : "+url.getProtocol());
			System.out.println("url.getQuery() : " + url.getQuery());
			System.out.println("url.getRef() : "+url.getRef());
			System.out.println("url.getUserInfo() : " + url.getUserInfo());
			System.out.println("url.toExternalForm() : "+url.toExternalForm());
			System.out.println("url.toURI() : "+url.toURI());
		} catch (Exception e) {

		}
	}
}

```

