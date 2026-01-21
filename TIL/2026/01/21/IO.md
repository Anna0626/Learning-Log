# IO

> 날짜: 2026-01-21
> 원본 노션: [링크](https://www.notion.so/IO-2efb28703eb080b1a896d1f1fd80aab9)

---

# FileReader

입력 스트림

```javascript
FileReader fr = new FileReader("파일경로");
```

## FileReader의 메소드

### read() 


| 읽는 단위 | 반환 값 |
| --- | --- |
| 문자 1개(1byte) | int(유니코드(ASCII 포함) 정수 값) , -1(파일 끝) |

## BufferedReader의 메소드

### readLine()


| 읽는 단위 | 반환 값 |
| --- | --- |
| 한 줄 | String, null(더 이상 읽을 줄이 없음) |

---

# FileWriter

출력 스트림, 메소드 : write()

```javascript
FileWriter fw = new FileWriter("파일경로");
```

예시1(덮어쓰기)

예시2(이어쓰기)

