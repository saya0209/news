package com.example.newsapp.controller;

import com.example.newsapp.model.News;
import com.example.newsapp.repository.NewsRepository;
import com.example.newsapp.service.CrawlingService;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class NewsController {

    private final NewsRepository newsRepository;
    private final CrawlingService crawlingService;

    // CrawlingService를 생성자 주입받도록 수정
    public NewsController(NewsRepository newsRepository, CrawlingService crawlingService) {
        this.newsRepository = newsRepository;
        this.crawlingService = crawlingService;
    }

    @GetMapping("/main.do")
    public String index(Model model) {
        // 데이터베이스에서 뉴스 리스트 가져오기
        List<News> newsList = newsRepository.findAll();
        System.out.println("뉴스 데이터: " + newsList); // 로그 출력

        // newsList를 모델에 추가
        model.addAttribute("newsList", newsList);

        return "main";
    }

    @GetMapping("/crawl")
    public String crawlNews(Model model) {
        // Python 스크립트 실행
        String output = crawlingService.executePythonScript();
        model.addAttribute("message", "크롤링 결과: " + output);
        
     // 데이터베이스에서 뉴스 리스트 가져오기
        List<News> newsList = newsRepository.findAll();
        System.out.println("뉴스 데이터: " + newsList); // 로그 출력

        // newsList를 모델에 추가
        model.addAttribute("newsList", newsList);
        
        return "redirect:/main.do";
    }
}
