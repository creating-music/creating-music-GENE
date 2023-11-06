package com.example.music.common.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class AuthenticationConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity httpSecurity) throws Exception{
        return httpSecurity
                .httpBasic().disable()// ui 인증 X 토큰 인증방식사용
                .csrf().disable()// get 요청을 제외한 post,put,delete 요청으로 부터 보호
                .cors().and()
                .authorizeRequests()
                .antMatchers("/users/login","/users/signup").permitAll() // 회원가입과 로그인은 허용
                .antMatchers(HttpMethod.POST,"/test").authenticated() //
                .and()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS) // jwt 사용시 사용
                .and()
                //    .addFilterBefore()
                .build();
    }
}
