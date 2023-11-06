package com.example.music.src.user;

import com.example.music.src.user.model.LoginReq;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     API 2 : 로그인
     */
    @PostMapping("/login")
    public String login(@RequestBody LoginReq loginReq){

        // todo : 검증

        // todo : 로그인


       return "로그인 완료";
    }


    @PostMapping("/signup")
    public String signup(){

        // todo : 검증

        // todo : 로그인

        return "회원가입 완료";
    }



}
