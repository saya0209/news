package com.example.newsapp.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Document(collection = "news")  // MongoDB 컬렉션 이름
@Data                           // Getter, Setter, toString 등을 자동 생성
@NoArgsConstructor              // 기본 생성자 자동 생성
@AllArgsConstructor             // 모든 필드를 초기화하는 생성자 자동 생성
public class News {
    @Id
    private String id;
    private String title;
    private String link;
    private String press;
    private String date;
    private String section;
    private String weather;
}
