package com.example.music.src.test;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/test")
public class TestController {


    @GetMapping("")
    public String getTest(){
        return "get test 성공";
    }

    @PostMapping("")
    public String postTest(){
        return "post test 성공";
    }
}
