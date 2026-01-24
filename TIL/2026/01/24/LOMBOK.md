# LOMBOK

> 날짜: 2026-01-24
> 원본 노션: [링크](https://www.notion.so/LOMBOK-2f2b28703eb080a09aded4b8b4b6c862)

---

# Lombok

어노테이션 기반으로 코드를 자동완성 해주는 라이브러리

- Getter, Setter, Equlas, ToString 등과 다양한 방면의 코드를 자동완성
- 롬복이 알아서 getter/setter를 생성 
- 변수 선언만 하면 모든 변수의 get/set를 생성해준다.
- 장점 
### @Data가 자동 완성 시켜주는 메소드 

- @ToString
- @EqualsAndHashCode
- @Getter
- @Setter
- @RequiredArgsConstructor
### 예시

1. java -jar lombok.jar 실행 -> IDE 선택
1. 롬복 import
```sql
package db;

import java.time.LocalDateTime;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BoardDTO {
	private int board_no, board_read;
	private String board_title, board_writer;
	private LocalDateTime board_date;
	
}

```



