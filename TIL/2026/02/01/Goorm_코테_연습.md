# Goorm 코테 연습

> 날짜: 2026-02-01
> 원본 노션: [링크](https://www.notion.so/Goorm-2f9b28703eb080708092e1bc107a056a)

---

### 초콜릿 포장

```java
import java.io.*;
import java.util.*;

class Main {
	public static void main(String[] args) throws Exception {
		int result = 0;
		int sum = 0;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st = new StringTokenizer(br.readLine());
		int choco = Integer.parseInt(st.nextToken()); 
		int box = Integer.parseInt(st.nextToken()); 
		ArrayList<Integer> size = new ArrayList<>();

		for(int i = 0; i <box; i++){
			st = new StringTokenizer(br.readLine());
			int width = Integer.parseInt(st.nextToken()); 
			int height = Integer.parseInt(st.nextToken()); 
			size.add(width*height);
			sum += width*height;
		}

		Collections.sort(size, Collections.reverseOrder());
		if(sum < choco){
			System.out.println("-1");
			return;
		}
		for(int i =0; i <box; i++){
			if(size.get(i) >= choco){
				result++;
				break;
			}else {
				choco -= size.get(i);
				result++;
			}
		}

		System.out.println(result);
	}
}
```

### 학생 정보 관리 어플리케이션

```java
import java.io.*;
import java.util.*;
class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		int num = Integer.parseInt(br.readLine());
		String[] opt = new String[num];
		String[] name = new String[num];
		for(int i = 0; i< num; i++){
			StringTokenizer st = new StringTokenizer(br.readLine());
			opt[i] = st.nextToken();
			name[i] = st.nextToken();
		}

		LinkedList<Integer> result = new LinkedList<>();
		int count = 0; 
		for(int i = num-1; i>=0; i--){
			if(opt[i].equals("find")){
				for(int j = 0; j<i; j++){
					if(opt[j].equals("add") && name[j].startsWith(name[i])){
						count++;
					}
				}
				result.addFirst(count);
				count =0;
			}else{
			}
		}
		

		for(Integer i : result){
			System.out.println(i);
		}
		
	}
}
```

