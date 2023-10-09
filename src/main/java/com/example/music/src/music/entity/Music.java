package com.example.music.src.music.entity;

import com.example.music.common.entity.BaseEntity;
import com.example.music.src.user.entity.User;
import lombok.Getter;
import org.springframework.web.bind.annotation.CrossOrigin;

import javax.persistence.*;

@Entity
@Getter
@Table(name = "Music")
public class Music extends BaseEntity {

    @Id @GeneratedValue
    @Column(name = "music_id")
    private Long id; // 음악에 대한 고유값 pk

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user; // 작곡자

    @Column(nullable = false)
    private String musicName; // 음악 이름 (사용자가 작성한 이름)

    @Column(name = "music_url",nullable = false)
    private String musicUrl; // 음악이 저장된 경로 (저장 위치)

    @Column(nullable = false)
    private boolean visible;

    @Column(name = "cover_url")
    private String coverUrl; // 음악 사진






}
