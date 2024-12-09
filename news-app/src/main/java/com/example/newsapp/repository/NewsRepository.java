package com.example.newsapp.repository;

import com.example.newsapp.model.News;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface NewsRepository extends MongoRepository<News, String> {
    List<News> findBySection(String section);
}
