# PDF

> 날짜: 2026-01-21
> 원본 노션: [링크](https://www.notion.so/PDF-2efb28703eb080ddb610ce2dbf3ae002)

---

```javascript
package io;

import java.io.*;
import java.nio.charset.Charset;
import com.itextpdf.text.*;
import com.itextpdf.text.pdf.PdfWriter;
import com.itextpdf.tool.xml.*;
import com.itextpdf.tool.xml.css.StyleAttrCSSResolver;
import com.itextpdf.tool.xml.html.*;
import com.itextpdf.tool.xml.parser.XMLParser;
import com.itextpdf.tool.xml.pipeline.css.CssResolverPipeline;
import com.itextpdf.tool.xml.pipeline.end.PdfWriterPipeline;
import com.itextpdf.tool.xml.pipeline.html.*;

// itextPDF
/*
 * 1. css 파일 경로 확실하게...
 * 2. 폰트 파일 경로 확실하게...
 * 3. <body style="font-family:MalgunGothic">라고 해당 폰트 사용하겠다고 선언
 * 
 */
public class PDF01 {
	public static void main(String[] args) {
		// 한글은 서체를 연결해주어야 합니다.
		String htmlText = """
				<html>
					<head>
					</head>
					<body style="font-family:MalgunGothic">
						<div> print </div>
						<div> print 1 </div>
						<div> 한글 문제 </div>
						<div> print 3 </div>
					</body>
				</html>
				""";
		
		try (FileOutputStream fos = new FileOutputStream("c:\\Temp\\test.pdf")) {
			
			Document document = new Document(PageSize.A4, 10, 10, 10, 10);
			
			PdfWriter writer = PdfWriter.getInstance(document, fos);
			
			document.open();
			// css
			StyleAttrCSSResolver cssResolver = new StyleAttrCSSResolver();
			
			FileInputStream cssfos = new FileInputStream("c:\\temp\\test.css");
			cssResolver.addCss(XMLWorkerHelper.getCSS(cssfos));
			
			//font
			XMLWorkerFontProvider font 
							= new XMLWorkerFontProvider(XMLWorkerFontProvider.DONTLOOKFORFONTS);
			// html 한글 폰트(ttf)
			font.register("c:\\windows\\fonts\\malgun.ttf", "MalgunGothic");
			CssAppliersImpl cssAppliersImpl = new CssAppliersImpl(font);
			
			HtmlPipelineContext context = new HtmlPipelineContext(cssAppliersImpl);
			context.setTagFactory(Tags.getHtmlTagProcessorFactory());
			
			PdfWriterPipeline pipeline = new PdfWriterPipeline(document, writer);
			
			HtmlPipeline htmlPipeline = new HtmlPipeline(context, pipeline); //누락
			// css + pipeline
			CssResolverPipeline cssResolverPipeline = 
					new CssResolverPipeline(cssResolver, htmlPipeline);
			
			XMLWorker worker = new XMLWorker(cssResolverPipeline, true);
			
			XMLParser xmlParser = new XMLParser(true, worker, Charset.forName("UTF-8"));
			
			//print : html로 만든 내용을 pdf에 붙이기
			StringReader stringReader = new StringReader(htmlText);
			xmlParser.parse(stringReader);
			
			//document.add(new Paragraph("내용"));
			
			document.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e1) {
			e1.printStackTrace();
		} catch (DocumentException e) {
			e.printStackTrace();
		}
	}
}
```

```css
div{
	background-color : blue;
	color : gray;
}
```

