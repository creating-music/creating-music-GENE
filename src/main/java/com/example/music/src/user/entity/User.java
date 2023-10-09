package com.example.music.src.user.entity;

import com.example.music.common.entity.BaseEntity;
import lombok.Getter;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import java.util.UUID;

@Getter
@Entity
@Table(name = "User")
public class User extends BaseEntity {

    @Id
    @GeneratedValue
    @Column(name = "user_id")
    private Long id; // 유저 table  pk

    @GeneratedValue(generator = "uuid2")
    @GenericGenerator(name="uuid2", strategy = "uuid2")
    @Column(name = "user_uniq_id",columnDefinition = "BINARY(16)",nullable = false)
    private UUID userUniqId; // 유저 uuid

    @Column(nullable = false)
    private String nickname; // 유저 이름

    @Column(nullable = false)
    private String email; // 유저 이메일


    @Enumerated(EnumType.STRING)
    private SocialLoginType socialLoginType;

    @Column(nullable = false)
    private String password; // 비밀번호 (암호화 해서 저장)

    @Column(name = "profile_url")
    private String profile; // 프로필 이미지 주소


    public enum SocialLoginType {
        LOCAL,
        KAKAO,
        NAVER,
        GOOGLE
    }


}
