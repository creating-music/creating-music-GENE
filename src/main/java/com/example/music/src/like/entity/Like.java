package com.example.music.src.like.entity;

import com.example.music.src.music.entity.Music;
import com.example.music.src.user.entity.User;
import lombok.Getter;

import javax.persistence.*;

@Getter
@Entity
@Table(name = "Like")
public class Like {

    @Id @GeneratedValue
    @Column(name = "like_id")
    private Long id;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;

    @OneToOne
    @JoinColumn(name = "music_id")
    private Music music;



}
