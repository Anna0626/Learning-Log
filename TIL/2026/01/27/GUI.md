# GUI

> 날짜: 2026-01-27
> 원본 노션: [링크](https://www.notion.so/GUI-2f5b28703eb0807e9e3ae2c2e68fcbdb)

---

# GUI

그래픽 사용자 인터페이스

### 자바로 그리는 그래픽

- AWT
- Swing
- javaFX

| 컨테이너 | 창 | frame, window, panel, dialog |
| --- | --- | --- |
| 컴포넌트 | 실제 컨테이너 위에 올려져서 화면 구성을 담당하는 요소 | Button, TextFiled, TextArea |
| 레이아웃 | 컨테이너 위의 컴포넌트를 어떻게 배치할 것인가 배치 전략 | GridLayout, BoardLayout |

---

# JFrame

Java Swing클래스의 일부이며, 구현되는 하나의 창

- Swing은 자바에서 그래픽 사용자 인터페이스를 구현하기 위해 제공되는 클래스 
- 컴포넌트 사용 가능
```java
import javax.swing.*;

JFrame frame명 = new JFrame();
```

## JFrame 요소 

### frame 사이즈 설정

```java
frame명.setSize(width,heigth);
```

### 창의 X누르면 창 닫히기

```java
frame명.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
```

### frame에 컴포넌트 넣기 

```java
frame명.add(컴포넌트명);
```

### 화면에 출력 

```java
frame명.setVisible(true);
```

---

# JButton

```java
JButton button명 = new JButton();
```

### 버튼을 클릭 시 이벤트 

```java
button.addActionListener(new ActionListener() {
			//클릭 시 실행 코드
});
```

---

# flow layout

붙이는 순서대로 출력 

- 컴포넌트들이 왼쪽에서 오른쪽으로 추가된다.
- 컨테이너 크기가 변경되면 컴포넌트 크기는 고정되고, 위치만 변경된다. 
- 기본적으로 중앙 정렬이다. 
```java
frame명.setLayout(new FlowLayout());
```

### 요소 넣기

```java
frame명.add(new 컴포넌트());
```

---

# Container

```java
Container container명 = frame명.getContentPane();
```

---

# Border Layout 

북쪽의 North , 중심의 Center, 남쪽의 South , 서쪽의 West , 동쪽의 East로 구성

- 각 영역에는 하나의 컴포넌트가 들어간다. 
- 중앙만 존재한다면 남은 공간을 모두 차지한다. 
- 위치 지정을 하지 않으면 중앙에 위치 
- .add(컴포넌트,위치)
```java
container명.add(컴포넌트명, BorderLayout.NORTH);
container명.add(컴포넌트명, BorderLayout.SOUTH);
container명.add(컴포넌트명, BorderLayout.WEST);
container명.add(컴포넌트명, BorderLayout.EAST);
container명.add(컴포넌트명, BorderLayout.CENTER);
```

---

# GridLayout

```java
frame명.setLayout(new GridLayout(행의 수,열의 수));
```

---

## 여러 요소 배치 

```java
public class Layout04 {
	JFrame frame = new JFrame("여러 배치 요소");
	JPanel jPanel = new JPanel();
	JButton[] button = new JButton[6];
	
	public Layout04() {
		for (int i = 0; i < button.length; i++) {
			button[i] = new JButton(i+ "번째 버튼");
		}
		
		jPanel.add(button[0]);
		jPanel.add(button[1]);
		jPanel.add(button[2]);
		jPanel.add(button[3]);
		
		frame.add(jPanel, "North");
		frame.add(button[4], "West");
		frame.add(button[5], "Center");
		
		frame.setSize(300,600);
		frame.setVisible(true);
	}
	public static void main(String[] args) {
		new Layout04();
	}
}
```

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/cb3b2870-3eb0-815c-99e6-0003045e9130/87ba6a58-06f4-45d0-9b84-12322fdcb51a/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466VBGEKXZU%2F20260128%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260128T004723Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQD0%2BT5QBigtwgTHUQwSZdfPcPaJk%2BcYJ0nPwwsrQjP2VgIhAKrwxOQV3u3dy5Y%2BH8pYqG7pKLX2uv1jJ3%2Bh4CSxSKxIKv8DCGEQABoMNjM3NDIzMTgzODA1Igzsx7pYMAN%2F9K2jLuAq3AMh293i7AOka3Ovl%2FPKdyq%2Bn2yOz91xZwrOBVnEKi4Suhn7EQPkI4FROxlYGuP2C2TwZKYnQbB3Btku2ByfvEZZCxSECU6gNyYMViJ%2FRK165pRiP1R6sow1heLCBVj5IipL%2BGXU4yPsb0tilQxUzfO5AlQNKD1tPyfrJ2egUCDryT%2FjS5TSOrhmF8Ph0yhWt8nNJzi3YFCXxpDJuTqXbsBoGs1KgreSLlb9BPPXw6dagd8QMxVYQsM6U%2BteqFtnRUVs%2FVE1LfIUoPFYqvOb0oNbhzjvOQM7VOC1nBn3uS%2F1uz%2Bni8jvVu3csm0X225XxCsIo9UZQuNOcNVs0a%2BewVeCLgxk7KxNL423thAcbeXyFFqCyJWdW6X9u39UpCZbgKMr0DVym1Bcx2B%2FO%2Flj9TwG0GMmsWnF7zJA0UOUdTm%2BBVRLPRmVeIebKFcdDYwE1cHvVvBOfoJMaWxLgcjGEBCjtMBFeHoapw%2BqN0OssRKGzbnY42chTtFkJ2J%2FboH8QKuOjitxUefHhtnEm1iN1QoAJ62REKhubzSeMI0mGzOvdDuhS8Gwa3rsLt72Jj%2Fk0IrfUFjMY0S80EvhtvZUiBv6ESHwUl%2FDKHC9bLcmG%2F7v5Oef9A4r%2BGW3BGPMzTD4mOXLBjqkAbCjWvGBc%2FT%2FHk2711wIgnWtIt6eixAAt1KENjpB7UGq%2FWhz8TPl9afZma5QptWNsujek69JCp4hyyqxVayDkUr5LEvZfQP822LeflIT8xXrMldPUNgBft9pj%2FyCepMiyH4Zpu3gpeROX7B7aiIB%2BctL7dOdzJY5LchNpGSa2INyb9fQIOfmQQ8JNB2MrHgGOci%2F%2BweYV1xPjc9dgwSXCKcp3AH%2B&X-Amz-Signature=be6021fa071e0aa8e8b547387abb8637c07e5e5bc16bc84553b541e39d12306b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

# FileDialog

```java
FileDialog open = new FileDialog(this, "open");
```

```java
FileDialog save = new FileDialog(this, "save", FileDialog.SAVE);
```

```java
// 폴더 
open.getDirectory()
// 파일
open.getFile()
```



