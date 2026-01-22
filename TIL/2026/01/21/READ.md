# READ

> 날짜: 2026-01-21
> 원본 노션: [링크](https://www.notion.so/READ-2efb28703eb080dfa3b2c64a50dcc8b2)

---

## Select A From B 

B 테이블에서 A 필드의 데이터 가져오기 

```sql
SELECT * From 테이블명;
SELECT 컬럼명 FROM 테이블명;
```

### COUNT

### AS 

별칭(alias)을 붙이기 

```sql
SELECT 컬럼명 AS 별칭
FROM 테이블명 AS 별칭;
```

### CONCAT

여러 문자열을 하나의 문자열로 결합

```sql
CONCAT(문자열1, 문자열2, ...)
```

### DISTINCT

중복을 제거하고 유일한 값만 조회

```sql
SELECT DISTINCT 컬럼명 
FROM 테이블명;
```



---

## Where

필터 역할을 하는 쿼리문

### 비교 연산자


| = | 특정값과 동일한 데이터 찾기 |
| --- | --- |
| <> | 특정값을 제외한 데이터 찾기 |
| >, <, <=, ≥ | 특정값과 비교해 데이터 찾기 |


| IS (NOT) NULL | NULL을 찾거나 제외할 때 |
| --- | --- |
| NOT | 제외하고 필터링할 때 |
| LIKE | 특정값을 포함한 값을 필터링할 때 |
| AND | 모두 참 |
| OR | 하나라도 참 |


| 'a%' | a로 시작하는 문자열 |
| --- | --- |
| '%a' | a로 끝나는 문자열 |
| '%a%' | a를 가진 문자열 |
| 'a%b' | a로 시작하고 b로 끝나는 문자열 |
| '_a%' | 두번째 문자가 a인 문자열 |
| '[abc]%' | 시작 문자가 a || b || c인 문자열 |
| '[a-f]%' | 시작 문자가 a와 f 사이인 문자열 |
| '[!abc]%' | 시작 문자가 a && b && c가 아닌 문자열 |

### IN

리스트의 값들과 일치하는 데이터를 필터링

```sql
WHERE 컬럼명 IN ("특정값_1", "특정값_2")
```

### BETWEEN A AND B

a와 b사이의 데이터 찾기 

```sql
WHERE 컬럼명 BETWEEN A AND B
```

---

## Order By

데이터 결과를 어떤 기준으로 정렬하여 출력할지 결정


| 오름차순 | 내림차순 |
| --- | --- |
| default | DESC |

---

## LIMIT

조회 결과의 개수를 제한

```sql
SELECT 컬럼명
FROM 테이블명
LIMIT 개수;
```

### 페이징


| limit 0, 10 | 1~10 |
| --- | --- |
| limit 10, 10 | 11~20 |
| limit 20, 10 | 21~30 |

---

# SELECT

## if

```java
SELECT if(조건식, 참, 거짓)
```

### 예시 

employees 테이블에서 gender가 ‘M’이면 ‘남자’ 아니면 ‘여자’로 출력

```java
SELECT if(gender = 'M' , '남자', '여자') AS 성별, s.last_name  
FROM employees s
LIMIT 2;
```


| 성별 | last_name |
| --- | --- |
| 남자 | Facello |
| 여자 | Simmel |

## AVG(평균)

```java
SELECT AVG(컬럼명)
```

### 예시

salaries 테이블의 salary의 평균 구하기 

---

# GROUP BY

특정 열을 기준으로 데이터를 그룹화

```java
SELECT 그룹기준컬럼, 집계함수(컬럼)
FROM 테이블명
GROUP BY 그룹기준컬럼;
```

### 예시

---

# DUAL(가상 테이블)

실제 데이터가 존재하지 않는 단일 행(one row), 단일 컬럼(dummy column)을 가진 가상 테이블

- 연산 결과를 출력하기 위한 용도
### DUAL의 구조

```java
테이블명 : DUAL
컬럼명   : DUMMY
행 개수  : 1행
값       : 'X'
```

### DUAL의 기본 사용 형태

```java
SELECT 표현식
FROM DUAL;
```

### 예시 



