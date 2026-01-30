# Goorm 코테 연습 

> 날짜: 2026-01-30
> 원본 노션: [링크](https://www.notion.so/Goorm-2f8b28703eb0807eb31ceb20bf1a3a0f)

---

### [KOI 2017] 딱지놀이

```java
import java.io.*;
import java.util.*;
class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		int round = Integer.parseInt(br.readLine());
		
		ArrayList<ArrayList<Integer>> shape = new ArrayList<>();
		for(int i =0; i<round*2; i++){
			StringTokenizer st = new StringTokenizer(br.readLine());
			int shapeC = Integer.parseInt(st.nextToken());
			ArrayList<Integer> list = new ArrayList<>();
			for(int j =0; j<shapeC; j++){
				list.add(Integer.parseInt(st.nextToken()));
			}
			shape.add(list);
		}

		ArrayList<String> win = new ArrayList<>();

		for (int i = 0; i < round * 2; i += 2) {
		
		    ArrayList<Integer> a = new ArrayList<>(shape.get(i));
		    ArrayList<Integer> b = new ArrayList<>(shape.get(i + 1));
		
		    Collections.sort(a, Collections.reverseOrder());
		    Collections.sort(b, Collections.reverseOrder());
		
		    int time = 0;
		    boolean decided = false;
		
		    while (!decided) {
		
		        if (time >= a.size() && time >= b.size()) {
		            win.add("D");
		            break;
		        } else if (time >= a.size()) {
		            win.add("B");
		            break;
		        } else if (time >= b.size()) {
		            win.add("A");
		            break;
		        }
		
		        if (a.get(time) > b.get(time)) {
		            win.add("A");
		            decided = true;
		        } else if (a.get(time) < b.get(time)) {
		            win.add("B");
		            decided = true;
		        } else {
		            time++;
		        }
		    }
		}

		for(String str : win){
			System.out.println(str);
		}
	}
}
```

### 인공지능 청소기 

```java
import java.io.*;
import java.util.*;
class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		int testCount = Integer.parseInt(br.readLine());
		ArrayList<ArrayList<Integer>> list = new ArrayList<>();
		String[] goal = new String[testCount];
 		for(int i =0; i<testCount; i++){
			ArrayList<Integer> t = new ArrayList<>();
			StringTokenizer st = new StringTokenizer(br.readLine());
			t.add(Integer.parseInt(st.nextToken()));
			t.add(Integer.parseInt(st.nextToken()));
			t.add(Integer.parseInt(st.nextToken()));
			list.add(t);
		}

		for(int i = 0; i<testCount; i++){
			ArrayList<Integer> test = new ArrayList<Integer>(list.get(i));
			if((Math.abs(test.get(0)) + Math.abs(test.get(1))) > test.get(2)) {
				goal[i] = "NO";
			}else if ((test.get(2)-(Math.abs(test.get(0)) + Math.abs(test.get(1))))% 2 != 0){
				goal[i] = "NO";
			}else {
				goal[i] = "YES";
			}
		}

		for(String s : goal){
			System.out.println(s);
		}
	}
}
```

### 방 배정하기

```java
import java.io.*;
import java.util.*;
class Main {
	public static void main(String[] args) throws Exception {
		int succes = 0;
		
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st = new StringTokenizer(br.readLine());
		int num1 = Integer.parseInt(st.nextToken());
		int num2 = Integer.parseInt(st.nextToken());
		int num3 = Integer.parseInt(st.nextToken());
		int student = Integer.parseInt(st.nextToken());

		for(int i =0; i<=student/num1; i++){
			for(int j =0; j<=student/num2; j++){
				int remain = student - num1*i - num2*j;
				if(remain<0){
					break;
				}
				if(remain % num3 == 0){
					succes = 1;
					System.out.println(succes);
					return;
				}
			}
		}
		System.out.println(succes);
	}
}
```

### 방 배정

```java
import java.io.*;
import java.util.*;

class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int studentC = Integer.parseInt(st.nextToken());
        int maxC = Integer.parseInt(st.nextToken());

        // 0~5: 여학생 1~6학년, 6~11: 남학생 1~6학년
        int[] sum = new int[12];

        for (int i = 0; i < studentC; i++) {
            st = new StringTokenizer(br.readLine());
            int gender = Integer.parseInt(st.nextToken());
            int grade = Integer.parseInt(st.nextToken());

            int index = (gender == 0) ? grade - 1 : grade + 5;
            sum[index]++;
        }

        int count = 0;
        for (int i = 0; i < sum.length; i++) {
            if (sum[i] > 0) {
                count += (sum[i] + maxC - 1) / maxC;
            }
        }

        System.out.println(count);
    }
}

```

```java
import java.io.*;
import java.util.*;
class Main {
	//한방 최대 인원 수 : k
	//모든 학생 배정하기 위한 방의 최소 개수 
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st = new StringTokenizer(br.readLine());
		int studentC = Integer.parseInt(st.nextToken());
		int maxC = Integer.parseInt(st.nextToken());
		ArrayList<ArrayList<Integer>> list = new ArrayList<>();
		for(int i =0; i<studentC; i++){
			ArrayList<Integer> stu = new ArrayList<>();
			st = new StringTokenizer(br.readLine());
			stu.add(Integer.parseInt(st.nextToken()));
			stu.add(Integer.parseInt(st.nextToken()));
			list.add(stu);
		}
		int[] sum = new int[12];
		for(int i =0; i<studentC; i++){
			ArrayList<Integer> student = new ArrayList<>(list.get(i));
			if(student.get(0) == 0){ //여
				sum[student.get(1)-1] += 1;
			}else{ //남
				sum[student.get(1)+5] += 1;
			}
		}

		int count = 0;
		for(int i =0; i<sum.length; i++){
			if(sum[i]>maxC){
				if(sum[i]%maxC != 0){
					count += sum[i]/maxC;
					count++;
				}else{
					count += sum[i]/maxC;
				}
			}else if(sum[i] != 0){
				count++;
			}
		}
		System.out.println(count);

	}
}
```

