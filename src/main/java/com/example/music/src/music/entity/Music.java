package com.example.music.src.music.entity;

import com.example.music.common.entity.BaseEntity;
import com.example.music.src.user.entity.User;
import lombok.Getter;

import javax.persistence.*;

@Entity
@Getter
@Table(name = "Music")
public class Music extends BaseEntity {

    @Id @GeneratedValue
    @Column(name = "music_id")
    private Long id; // 음악에 대한 고유값 pk

    @Column(name = "music_name")
    private String musicName; // 음악 이름 (사용자가 작성한 이름)


    private String field; // 음악이 저장된 경로 (저장 위치)


    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user; // 작곡자





}
