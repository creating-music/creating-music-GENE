package com.example.music.src.member.entity;

import com.example.music.common.entity.BaseEntity;
import lombok.Getter;

import javax.persistence.*;

@Getter
@Entity
@Table(name = "Member")
public class Member extends BaseEntity {

    @Id
    @GeneratedValue
    private Long id; // 유저 고유 식별값 pk

    @Column(nullable = false)
    private String nickname; // 유저 이름

    @Column(nullable = false)
    private String email; // 유저 이메일


    @Enumerated(EnumType.STRING)
    private SocialLoginType socialLoginType;

    @Column(nullable = false)
    private String password; // 비밀번호 (암호화 해서 저장)


    public enum SocialLoginType {
        LOCAL,
        KAKAO,
        NAVER,
        GOOGLE
    }







}
