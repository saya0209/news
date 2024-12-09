<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>뉴스 대시보드</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-4">
        <h1 class="text-center">뉴스 대시보드</h1>

        <!-- 크롤링 버튼 -->
        <div class="text-center mb-4">
            <a href="/crawl" class="btn btn-primary">새로고침</a>
        </div>

        <!-- 성공 메시지 -->
        <c:if test="${not empty message}">
            <div class="alert alert-success text-center">
                ${message}
            </div>
        </c:if>

        <!-- 뉴스 리스트 -->
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>제목</th>
                    <th>언론사</th>
                    <th>날짜</th>
                    <th>링크</th>
                    <th>날씨</th>
                </tr>
            </thead>
            <tbody>
                <c:forEach var="news" items="${newsList}">
                    <tr>
                        <td>${news.title}</td>
                        <td>${news.press}</td>
                        <td>${news.date}</td>
                        <td><a href="${news.link}" target="_blank">기사 보기</a></td>
                        <td>${news.weather}</td>
                    </tr>
                </c:forEach>
            </tbody>
        </table>
    </div>
</body>
</html>
