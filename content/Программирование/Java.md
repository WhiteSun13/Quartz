#Программирование 
[Youtube Bro Code](https://www.youtube.com/watch?v=xk4_1vDrzzo&ab_channel=BroCode)

```java
import java.util.Scaner;

Scaner scaner = new Scaner(System.in);

String x = scaner.next();

// Сравнение
x = "Q"
x.equals("Q");
x.equalsIgnoreCase("q");

x.lenght();
x.chartAt(index);
x.indexOf(chart)
x.isEmpty()

x.toUpperCase()
x.toLowerCase()

x.trim() // Убрать все пробелы, например "    Bro    " -> "Bro"
x.replace("o","a") // Заменить символы
```
# Простой UI

```java
import javax.swing.JOptionPane;

public class Main {
	public static void main(String[] args) {
		String name = JOptionPane.showInputDialog("Enter your name"); 
		JOptionPane.showMessageDialog(null, "Hello "+name);
		int age = Integer.parseInt(JOptionPane.showInputDialog("Enter your age"));
		JOptionPane.showMessageDialog(null, "You are "+age+" years old");
		double height = Double.parseDouble(JOptionPane.showInputDialog("Enter your height"));
		JOptionPane.showMessageDialog(null, "You are "+height+" cm tall");
	}
}
```

# Random

```java
import java.util.Random;

Random random = new Random();

int x = random.nextInt(6);
double y = random.nextDouble();
boolean z = random.nextBoolean();
```
# If statement

```java
if(age>=75){
	System.out.println("Ok Boomer!")
}
else if(age>=18){
	System.out.println("You are an adult!")
}
else{
	System.out.println("You are not an adult!")
}
```
# Switch

```Java
String day = "Friday"

switch(day){
case "Sunday": // Something;
break;
case "Monday": // Something;
break;
default: // Something
}
```

# JAR

```shell
jar cfe HelloWorld.jar HelloWorld HelloWorld.class HelloWorld.java
```

1. `jar`: Это утилита Java для создания, извлечения и обновления JAR-файлов.

2. `cfe`: Эти буквы стоят за сокращением "create, fill, and execute". Они указывают действия, которые должна выполнить утилита `jar`.

- `c`: Создать новую архиву
- `f`: Указать имя файла архива
- `e`: Включить файл манифеста

3. `HelloWorld.jar`: Это имя создаваемого JAR-файла.

4. `HelloWorld`: Это основной класс, который будет включен в JAR-файл.

5. `HelloWorld.class`: Это скомпилированный файл класса Java, который будет включен в JAR.

6. `HelloWorld.java`: Это исходный файл кода Java, который также будет включен в JAR.

### Ключевые моменты

- Команда `jar cfe` обычно используется для создания самодостаточного исполняемого JAR-файла.
- Включение как скомпилированного (.class), так и исходного кода (.java) файла в JAR позволяет более легко отлаживать и поддерживать программу.
- Специфицированный основной класс (HelloWorld в данном случае) становится точкой входа в JAR-файл.

### Лучшие практики

1. Всегда явно указывайте основной класс при создании JAR-файла для запуска.
2. Включайте как скомпилированные, так и исходные кодовые файлы в JAR для лучшей поддерживаемости.
3. Используйте значительные имена для ваших JAR-файлов, отражающие их содержимое и назначение.
4. Рассмотрите возможность использования флага `-v` с командой `jar` для подробного вывода во время создания, особенно при работе с большими файлами или директориями.

### Пример использования

`java -jar HelloWorld.jar`

Это предполагает, что класс `HelloWorld` имеет метод `main`, определенный внутри него.
## 2 класса в 1 программе

```bash
jar cfe Programs.jar First First.class First.java Second.class Second.java
```
**Запуск**
```bash
java -cp Programs.jar First
java -cp Programs.jar Second
```

# Массив

```Java
String[] cars = {"Lada", "BMW", "Tesla"};
String[] cars = new String[3];

cars.length;

String[][] = new String[3][3];
```

# ArrayList

Хранит ссылочные данные (Integer, Double, Boolean, Character, String)
```Java
ArrayList<String> food = new ArrayList<String>();

food.add("pizza");
food.set(0, "sushi");
food.remove(2);
food.clear();

for(int i=0; i<food.size(); i++){
	System.out.println(food.get(i));
}
```