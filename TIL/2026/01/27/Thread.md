# Thread

> 날짜: 2026-01-27
> 원본 노션: [링크](https://www.notion.so/Thread-2f5b28703eb080eba23af4f9911ce072)

---

# Thread

프로세스(process) 내에서 실제로 작업을 수행하는 주체를 의미

- 모든 프로세스에는 한 개 이상의 스레드가 존재하여 작업을 수행
- 멀티스레드 프로세스(multi-threaded process) : 두 개 이상의 스레드를 가지는 프로세스


## Thread 생성 

### 방법 1) Runnable 인터페이스를 구현하는 방법

```java
class A implements Runnable{
	@Override
	public void run() {
	}
}
```

```java
Thread a = new Thread(new A());  //Runnable 인터페이스를 구현
a.start(); //스레드의 실행
```

### 방법 2) Thread 클래스를 상속받는 방법

```java
class B extends Thread{
	@Override
	public void run() {
	}
}
```

```java
B b = new B();  //Thread 클래스를 상속
b.start(); //스레드의 실행
```

---

# Synchronized

lock을 이용해 동기화를 수행

### synchronized method

인스턴스 단위로 lock 공유 

```java
public class Method {
    public static void main(String[] args) {
        Method method1 = new Method();
        Method method2 = new Method();

        Thread thread1 = new Thread(() -> {
            System.out.println("스레드1 시작 " + LocalDateTime.now());
            method1.syncMethod1("스레드1");
            System.out.println("스레드1 종료 " + LocalDateTime.now());
        });

        Thread thread2 = new Thread(() -> {
            System.out.println("스레드2 시작 " + LocalDateTime.now());
            method2.syncMethod2("스레드2");
            System.out.println("스레드2 종료 " + LocalDateTime.now());
        });

        thread1.start();
        thread2.start();
    }

    private synchronized void syncMethod1(String msg) {
        System.out.println(msg + "의 syncMethod1 실행중" + LocalDateTime.now());
        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private synchronized void syncMethod2(String msg) {
        System.out.println(msg + "의 syncMethod2 실행중" + LocalDateTime.now());
        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```



### static 키워드가 포함된 synchronized method

인스턴스가 아닌 클래스 단위로 lock을 공유

```java

```

