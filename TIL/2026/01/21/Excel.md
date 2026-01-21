# Excel

> 날짜: 2026-01-21
> 원본 노션: [링크](https://www.notion.so/Excel-2efb28703eb080178443c11e0251d247)

---

# jxl.jar 라이브러리 

## write


| 이름 | 나이 |
| --- | --- |
| 홍길동 | 20 |
| 강감찬 | 15 |

```javascript
package io;

import java.io.*;
import java.util.*;
import jxl.*;
import jxl.write.*;

public class Excel01 {
	public static void main(String[] args) {
		WritableWorkbook workbook = null;
		WritableSheet sheet = null;
		File file = new File("c:\\Temp\\excel01.xls");
		
		Map<String, String> map = new HashMap<String, String>();
		map.put("이름", "홍길동");
		map.put("나이", "20");
		
		Map<String, String> map2 = new HashMap<String, String>();
		map2.put("이름", "강감찬");
		map2.put("나이", "15");
		
		List<Map<String, String>> list = new ArrayList<Map<String,String>>();
		list.add(map);
		list.add(map2);
		
		// 파일 만들기 쓰기
		try {
			workbook = Workbook.createWorkbook(file);
			workbook.createSheet("시트", 0);
			sheet = workbook.getSheet(0);
			
			Label label = new Label(0, 0, "이름");
			sheet.addCell(label);
			label = new Label(1, 0, "나이");
			sheet.addCell(label);
			
			// 데이터 붙이기
			for (int i = 0; i < list.size(); i++) {
				 Map<String, String> e = list.get(i);
				 label = new Label(0, (1 + i), e.get("이름"));
				 sheet.addCell(label);
				 label = new Label(1, (1 + i), e.get("나이"));
				 sheet.addCell(label);
			}
			
			// 쓰기
			workbook.write();
			// 닫기
			workbook.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
```

이름 칸(0,0) → Label label = new Label(0.0, "이름");



## read


| 이름 | 나이 |
| --- | --- |
| 홍길동 | 20 |
| 강감찬 | 15 |

```javascript
package io;

import java.io.*;
import jxl.*;
import jxl.read.biff.BiffException;

public class Excel02 {
	public static void main(String[] args) {
		Workbook workbook = null;
		try {
			workbook = Workbook.getWorkbook(new File("c:\\Temp\\excel01.xls"));
			//sheet 
			Sheet sheet = workbook.getSheet(0);
		
			for(int i = 0; i < sheet.getRows(); i++) {
				for (int j = 0; j<sheet.getColumns(); j++) {
					Cell cell = sheet.getCell(j,i);
					System.out.print(cell.getContents()+ "\t");
				}
				System.out.println(""); //엔터 처리
			}
		} catch (BiffException | IOException e) {
				e.printStackTrace();
		}
	}
}
```

출력 결과: 

```javascript
이름	  나이	
홍길동	  20	
강감찬	  15	
```

(a,b) 위치의 내용 

```javascript
Cell cell2 = sheet.getCell(a,b);
System.out.println("0,0 cell : "+cell2.getContents());

//한 줄로 
sheet.getCell(a,b).getContents();
```


| 행의 수 | sheet명.getRows() |
| --- | --- |
| 열의 수 | sheet명.getColumns() |
| (a,b) 위치의 셀(Cell) 객체를 가져옴 | sheet명.getCell(a,b) |
| 셀 안에 들어있는 값을 문자열(String)로 반환 | cell명.getContents() |

# poi-4.0.0.jar 라이브러리 

- HSSFWorkbook() : 2003버전 이전 : xls
- XSSFWorkbook() : 2003버전 이후 : xlsx : 읽기/쓰기
- SXSSFWorkbook() : 대용량 : 정해진 용량 만큼 씩 호출해 사용 : 쓰기
## write


| 이름 | 나이 |
| --- | --- |
| 홍길동 | 20 |
| 강감찬 | 15 |

```javascript
package io;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;

import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;

public class Excel03 {
	public static void main(String[] args) {
		Workbook workbook = new HSSFWorkbook();
		Sheet sheet = workbook.createSheet("시트만들기");
		Row row = null;
		Cell cell = null;
		int rowNum = 0;
		
		row = sheet.createRow(rowNum++);
		cell = row.createCell(0);
		cell.setCellValue("이름");
		
		cell = row.createCell(1);
		cell.setCellValue("나이");
		
		//새로운 row
		row = sheet.createRow(rowNum++);
		cell = row.createCell(0);
		cell.setCellValue("홍길동");
		
		cell = row.createCell(1);
		cell.setCellValue(20);
		//새로운 row
		row = sheet.createRow(rowNum++);
		cell = row.createCell(0);
		cell.setCellValue("강감찬");
		
		cell = row.createCell(1);
		cell.setCellValue(15);
		
		// write
		try {
			File file = new File("c:\\Temp\\excel02.xls");   
			FileOutputStream fos = new FileOutputStream(file);
			workbook.write(fos);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
```

## read

```javascript
package io;

import java.io.*;
import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.ss.usermodel.*;

public class Excel04 {
	public static void main(String[] args) {
		try {
			Workbook wb = WorkbookFactory.create(new FileInputStream("c:\\Temp\\excel02.xls"));
			Sheet sheet = wb.getSheetAt(0);
			
			for (Row row : sheet) {
				for (Cell cell : row) {
					System.out.print(cell.toString() + "\t");
				}
				System.out.println(""); // enter
			}
			
		} catch (EncryptedDocumentException e) {
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
```

출력 결과:

```javascript
이름	  나이	
홍길동	  20.0	
강감찬	  15.0	
```



