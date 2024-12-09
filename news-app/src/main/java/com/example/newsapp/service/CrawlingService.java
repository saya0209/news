package com.example.newsapp.service;

import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@Service
public class CrawlingService {

    public String executePythonScript() {
        StringBuilder output = new StringBuilder();
        try {
            // 첫 번째 Python 스크립트 실행
        	String pythonScript1 = new ClassPathResource("python/naver_news_crawler.py").getFile().getAbsolutePath();
        	String pythonScript2 = new ClassPathResource("python/weather_api_integration.py").getFile().getAbsolutePath();

        	Process process1 = Runtime.getRuntime().exec(new String[]{"python", pythonScript1});
            System.out.println("process1: " + process1);

            // 두 번째 Python 스크립트 실행
            Process process2 = Runtime.getRuntime().exec(new String[]{"python", pythonScript2});
            System.out.println("process2: " + process2);

            // 첫 번째 스크립트의 출력 읽기 (UTF-8 인코딩 지정)
            BufferedReader reader1 = new BufferedReader(
                    new InputStreamReader(process1.getInputStream(), "UTF-8")
            );
            System.out.println("reader1.readLine(): " + reader1.readLine());

            BufferedReader errorReader1 = new BufferedReader(new InputStreamReader(process1.getErrorStream(), "UTF-8"));
            String errorLine;
            while ((errorLine = errorReader1.readLine()) != null) {
                System.out.println("Error: " + errorLine);
            }

            String line1;
            while ((line1 = reader1.readLine()) != null) {
                System.out.println("line1: " + line1);  // 출력된 내용 확인
                output.append(line1).append("\n");
            }

            // 두 번째 스크립트의 출력 읽기 (UTF-8 인코딩 지정)
            BufferedReader reader2 = new BufferedReader(
                    new InputStreamReader(process2.getInputStream(), "UTF-8")
            );
            String line2;
            while ((line2 = reader2.readLine()) != null) {
                output.append(line2).append("\n");
            }

            // 두 프로세스 종료 대기
            process1.waitFor();
            process2.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
            return "Error occurred: " + e.getMessage();
        }

        return output.toString();
    }
}
