# Inner Class

> 날짜: 2026-01-22
> 원본 노션: [링크](https://www.notion.so/Inner-Class-2f0b28703eb0800d9158c08a79e93f62)

---

# 내부 클래스(Inner class)

클래스 내부에 선언된 클래스 (두 클래스가 긴밀한 관계)

- 장점
- 단점
## 클래스의 종류 

### static 클래스

- 외부 클래스의 멤버 변수 위치에 선언한다. 
- static 멤버처럼 다룬다.
- 특히 static 메소드에서 사용될 목적으로 선언한다. 
- 외부 클래스의 인스턴스 멤버에 접근할 수 없다.
### 멤버 클래스

- 외부 클래스의 멤버 변수 위치에 선언 
- 인스턴스 멤버처럼 활용
- 주로 외부 클래스의 인스턴스 멤버와 관련된 작업을 수행할 때 사용
### 로컬 클래스(지역 클래스)

- 외부 클래스의 메소드나, 초기화 블럭 안에서만 선언한다. 
- 선언된 메소드 영역에서만 사용 가능
### 익명 클래스

- 클래스 선언과 객체 생성을 동시에 하는 이른없는 클래스 
- 일회용 클래스


---

# Member Class

클래스 내부(멤버 변수 위치)에 선언된 클래스, 외부 클래스의 멤버변수 선언위치에 선언


| instance class | static class |
| --- | --- |
| 외부 클래스의 인스턴스멤버처럼 다룸 | 부 클래스의 static멤버처럼 다룸 |

# 정적 내부 클래스(static nested class)

class 앞에 static 키워드를 붙여서 선언한 내부 클래스

```java
class OutClass{
		static class InnerClass{
		}
}
```

- 객체 생성 없이 사용
- 클래스의 static 멤버처럼 다룸
- 외부 클래스와 내부 클래스는 다르게 동작 
- 외부 클래스와 내부 클래스의 멤버가 private라도 접근 가능
- 경로만 지정된다면 외부에서 단독으로 직접 호출 가능
- 외부 클래스의 인스턴스 멤버에 접근 불가
- 주로 외부 클래스의 static 멤버와 관련된 작업을 수행할 때 사용
### 내부 클래스의 static 멤버 접근 

```java
class OutClass {
	private static int age = 100;
	
	public static class InClass {
		static int number = 10;
	}
}

public class StaticClass01 {
	public static void main(String[] args) {
		OutClass outClass = new OutClass();
		OutClass.InClass inClass = new OutClass.InClass();
		inClass.number = 20;         //실행은 되지만 아래 방법을 권장
		OutClass.InClass.number = 20; //number = 20으로 변경
	}
}
```

위와 같은 방법으로 내부 클래스의 static 멤버에 접근을 할 수 있다. 

# 인스턴스 Member Class(non-static)

static 멤버를 사용하지 않는 클래스 

```java
class OutClass {
    private int value = 10;  // 외부 클래스의 인스턴스 멤버
   
    class InClass {  // 인스턴스 Member Class
        void print() {
		        // 외부 인스턴스 멤버 접근 가능
            System.out.println(value); 
        }
    }
}
```

- 인스턴스 속성 변수처럼 활용
- member 클래스는 외부 클래스의 인스턴스 멤버처럼 사용할 수 있지만 외부 클래스는 객체 생성 없이 내부 클래스의 멤버를 사용할 수 없다.
- static 붙은 메소드 내에서는 내부 클래스의 객체 선언은 할 수 없다. 
- 용도 : 외부 클래스의 인스턴스 멤버와 관련된 작업을 수행할 때 사용
- 특징 : 외부 클래스의 모든 멤버에 접근 가능 


---

# 지역 클래스(Local Class)

메소드 내부나 초기화 블럭 내부에 선언되는 클래스

```sql
class Outer {
    void method() {
        // 지역 클래스
        class Local {
            void print() {
                System.out.println("Local Class");
            }
        }
        // 지역 클래스 객체 생성
        Local local = new Local();
        local.print();
    }
}
```

- 선언한 메소드 안에서만 사용할 수 있다. 
- 지역 클래스는 블록 종료 시 제거된다. 
- 외부에서 인스턴스를 생성할 수 없다. 또한 static을 붙일 수 없다.
- 인스턴스 변수 또는 메소드는 사용할 수 있다. 
- 외부 클래스에서 final 붙은 지역 변수(상수)나 매개변수는 지역 클래스의 메소드에서 접근 가능
- 지역 클래스는 상속 불가
- 사용 시에는 객체를 생성한 후에 사용한다.  
- 내부 클래스는 컴파일 시 일부 외부 클래스$숫자+내부클래스명.class 파일로 생성
- 숫자는 서로 다른 메소드인 경우에 같은 이름의 클래스가 존재할 수 있어서 구분 용도
- 특징 : 선언된 메소드 블럭 안에서만 유효 
- 주의 : 메소드의 지역변수를 클래스 내부에서 사용할 때 해당 변수가 final 이거나 값이 변경되지 않아야 한다.
### 예시

```sql
public class LocalClass {
	//method
	public void outMethod() {
		//inner class
		class InClass{
			public void print() {
				System.out.println("Local Class");
			}
		}
		InClass inClass = new InClass();
		inClass.print();  //Local Class
	}
	public static void main(String[] args) {
		LocalClass localClass = new LocalClass();
		localClass.outMethod();

	}
}
```

---

# 익명 클래스(Anonymous Class)

이름이 없는 내부 클래스로, 클래스 선언과 객체 생성을 동시에 수행하는 클래스이다.

인터페이스 구현 형태

```java
인터페이스명 변수 = new 인터페이스명() {
    // 추상 메서드 구현
};
//인터페이스인 경우에는 인터페이스를 상속 받는 부모 클래스가 Object가 된다.
```

클래스 상속 형태

```java
클래스명 변수 = new 클래스명() {
    // 메서드 재정의
};
//new 뒤에 오는 생성자명이 기존 클래스명이면 익명 클래스가 자동으로 클래스의 하위 객체가 된다.
```

- 클래스 이름 없음
- 단 한 번만 사용, 객체를 한번만 사용하는 경우 사용 
- 객체 생성과 동시에 정의
- 둘 이상의 인터페이스를 가질 수 없다.
- 코드 블럭에 클래스 선언을 한다. 생성자를 호출하는 것과 같다.
- 특징 : 일회성으로 사용되는 인터페이스 구현체나 상속 클래스에 사용
- 장점 : 코드가 간결해지고, 일회성 클래스를 정의할 때 유용, UI 이벤트 처리나 스레드 생성시에 활용 
```sql
interface Greeting {
	void sayHello();
}

class B implements Greeting {
	@Override
	public void sayHello() {
	}
}

public class AnonymousClass {
	public static void main(String[] args) {
		B b = new B();
		Greeting g = new B();
		Greeting g2 = new Greeting() {
			@Override
			public void sayHello() {
				System.out.println("g2");
			}
		};
		g.sayHello();
		g2.sayHello();
		
		Greeting g3 = new Greeting() {
			@Override
			public void sayHello() {
				System.out.println("g3");
			}
		};
		
		g3.sayHello();
		g = g3; 
		g.sayHello();
		System.out.println(g3 == g);
	}
}
```

출력 결과: 

```sql
g2
g3
g3
true
```

---

# 정리


|  | 정적 클래스 | 인스턴스 클래스 | 지역 클래스 | 익명 클래스 |
| --- | --- | --- | --- | --- |
| 선언 위치 | 클래스 멤버 위치 | 클래스 멤버 위치 | 메서드 / 생성자 / 블록 내부 | 표현식 위치 |
| static 키워드 | O | X | X | X |
| 외부 객체 필요 | X | O | X | X |
| 외부 인스턴스 멤버 접근 | X | O | O | O |
| 외부 static 멤버 접근 | O | O | O | O |
| 객체 생성 방식 | new Outer.Inner() | o.new Inner() | new Local() | new 인터페이스(){} |
| 생성자 선언 | O | O | O | X |
| 접근 제한자 | O | O | X | X |
| 재사용 가능 | O | O | X | X |
| 상속/구현 | 클래스/인터페이스 | 클래스/인터페이스 | 클래스/인터페이스 | 클래스 1개 or 인터페이스 1개 |
| 주요 용도 | 외부 static 기능 묶기빌더 패턴 | 외부 객체 상태에 의존 | 메서드 내부 보조 클래스 | 1회용 객체, 이벤트 처리 |



