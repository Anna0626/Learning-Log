# IO

> 날짜: 2026-01-20
> 원본 노션: [링크](https://www.notion.so/IO-2eeb28703eb0806bb359e792030ad1ca)

---

# 자바와 외부를 연결

## java.io

- stream 기반 동작
- 데이터를 읽기 위해서 힙공간에 메모리 버퍼를 생성한다. 
- 데이터를 읽을 때까지 스레드가 차단(blocking)된다. 
## java.nio

- channel / buffer 기반 동작 
- Non-Blocking IO	

|  | 기존(IO) | 신규(NIO) |
| --- | --- | --- |
| 방식 | 스트림 | 버퍼 |
| 블로킹 여부 | 블로킹만 지원 | 블로킹/논믈로킹 둘 다 지원 |
| 흐름 | 입력/출력 스트림(단방향) | 채널 사용(양방향) |
| 사용처 | 사용자↓ 데이터↑ | 사용자↑ 데이터↓ |

### 처리 방식 


| IO로 처리할 때 | NIO로 처리할 때 |
| --- | --- |
| 연결되는 사용자 수가 적을 때 | 동시 사용자가 많을 때(채팅, 알림 등) |
| 데이터 용량이 크고 처리가 순차적이어야 할 때 | 운영체제 시스템 call을 줄여서 성능 최적화가 필요할 때 |
| 코드가 단순하고 직관적인 것이 중요할 때 | 많은 입출력을 관리할 때 |

## 스트림

스트림은 1byte씩 읽는다. 한 번 읽은 데이터 앞 뒤로 이동X

## 버퍼 

위치를 이동하며 필요한 부분만 골라서 읽기 가능 

## 블로킹 

read()를 사용해서 데이터가 들어올때까지 스레드가 대기 상태 

## 논 블로킹 

읽을 데이터가 없으면 바로 리턴, 다른 작업을 수행할 수 있음

## 셀렉터(Selector)

하나의 스레드가 여러 채널을 감시, 이벤트가 발생한 채널만 골라서 처리 

---

# JAVA IO

byte 기반 Stream 

재사용성이 높다. IO확장이 가능하다.

메모리 데이터를 스트림 기반 IO 구조로 추상화하여 파일이나 네트워크 IO와 동일한 방식으로 처리하기 위해 사용된다.

### 예시

```javascript

//byte 배열에서 읽어오기 
byte[] input = new byte[] {'A', -1, -128,18,16,12,9,7,6,2,1};
byte[] output = null;

//input 통로 생성 
ByteArrayInputStream bais = null;

//output
ByteArrayOutputStream baos = null;

//읽기/쓰기 시 바이트를 담을 변수 
int data = 0; //만약 데이터가 없다면 -1

bais = new ByteArrayInputStream(input);
baos = new ByteArrayOutputStream();   //read()를 통해서 읽기 

while(true) { 
	data = bais.read();   //data : byte -> int형으로 변환되어 들어있음
	System.out.println("data : "+ data);
	if(data == -1) { 
		break;
	}
	baos.write(data);
}

while((data = bais.read()) != -1 ) {
	baos.write(data);
}

output = baos.toByteArray();   //baos에 쌓아둔 요소들을 byte배열로 꺼냄 
//baos를 초기화 하고 싶다면 : baos.reset();

System.out.println(Arrays.toString(input));
System.out.println(Arrays.toString(output));
```

---

## try - catch - finally

단점 : 코드가 길어진다.

## try - with - resource 

자동 닫기 가능(리소스를 사용한 후 자동으로 닫아주는 기능)

불필요한 문을 자동을 닫아 주는 기능이 있어서 코드를 줄일 수 있다. 

- try() 괄호에 리소스를 선언
- 성공 여부와 상관없이 끝나면 자동으로 close()가 호출됨
### 실행 순서

try 블록 진입 -> 리소스 생성 -> 코드 실행 -> 예외 발생 여부와 상관 없이 close()호출 

### 특징

- 기존의 방식은 try블록과 finally블록 모두에서 예외가 발생하면 try의 예외가 무시되는 문제점이 있다. 
- 하지만 새로운 방식은 실제 발생한 모든 예외를 보존하고 close()시 발생한 예외는 억제된 예외로 기록/보관된다. 
### 예시

```javascript
class A implements AutoCloseable{
	@Override
	public void close() throws Exception {
		System.out.println("A 클래스 close();");
	}
	public void print() {
		System.out.println("A클래스 print()");
		System.out.println("A클래스 print()");
		System.out.println("A클래스 print()");
	}
}

public class IO02 {
	public static void main(String[] args) {
	
		//java 1.7
		try(A a= new A()) {
			a.print();
		} catch (Exception e) {
			System.out.println("예외가 발생했습니다.");
		}
		
		//java 1.9 :: 주의 a는 final만 가능 :: 값 변경이 없는 것 
		A a = new A();
		try(a) {
			a.print();
		} catch (Exception e) {
			System.out.println("예외가 발생했습니다.");
		}	
	}
}
```

출력 결과:

```javascript
A클래스 print()
A클래스 print()
A클래스 print()
A 클래스 close();
A클래스 print()
A클래스 print()
A클래스 print()
A 클래스 close();
```

### 차이점

try - with - resource 문을 활용하면 코드를 간결하게 할 수 있다. 

try - catch - finally

```javascript
byte[] input = { 1, 3, 4, 8, 9, 10, 15, 19, 20, 23 };
byte[] output = null;
// 읽기/쓰기 하는 배열
byte[] temp = new byte[3];

ByteArrayInputStream bais = null;
ByteArrayOutputStream baos = null;
bais = new ByteArrayInputStream(input);
baos = new ByteArrayOutputStream();

// 배열에 몇개 데이터를 저장했는지 확인하는 변수
int data = 0; 
try{
	while ((data = bais.read(temp)) != -1) {
		System.out.println("읽은 수 : " + data);
		System.out.println("temp: " + Arrays.toString(temp));
		baos.write(temp, 0, data);
	}
	// baos -> output
	output = baos.toByteArray();
} catch (IOException e) {
	e.printStackTrace();
} finally {
	try {
		bais.close();
	} catch (IOException e) {
		e.printStackTrace();
	}
	try {
		baos.close();
	} catch (IOException e) {
		e.printStackTrace();
	}
}
System.out.println(Arrays.toString(input));
System.out.println(Arrays.toString(output));
```

try - with - resource 

```javascript
byte[] input = { 1, 3, 4, 8, 9, 10, 15, 19, 20, 23 };
byte[] output = null;
// 읽기/쓰기 하는 배열
byte[] temp = new byte[3];

// 배열에 몇개 데이터를 저장했는지 확인하는 변수
int data = 0;
//try with resource : 자동 닫기 가능, 여러개 선언할 떄는 ";"붙여 나열한다.  
try (ByteArrayInputStream bais = new ByteArrayInputStream(input);
		ByteArrayOutputStream baos = new ByteArrayOutputStream();) {
	while ((data = bais.read(temp)) != -1) {
		System.out.println("읽은 수 : " + data);
		System.out.println("temp: " + Arrays.toString(temp));
		baos.write(temp, 0, data);
	}
	// baos -> output
	output = baos.toByteArray();
} catch (IOException e) {
	e.printStackTrace();
} 
System.out.println(Arrays.toString(input));
System.out.println(Arrays.toString(output));
```

---



