package com.example.music.src.playlist.entity;

import com.example.music.src.user.entity.User;

import javax.persistence.*;

@Entity
public class PlayList {

    @Id @GeneratedValue
    @Column(name = "playlist_id")
    private Long id;

    @Column(name = "playlist_name")
    private String name;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    private int visible;


}
