package com.example.music.src.playlist.entity;

import com.example.music.common.entity.BaseEntity;
import com.example.music.src.user.entity.User;
import lombok.Getter;

import javax.persistence.*;
@Getter
@Entity
@Table(name = "PLAYLIST")
public class PlayList extends BaseEntity {

    @Id @GeneratedValue
    @Column(name = "playlist_id")
    private Long id;

    @Column(nullable = false)
    private String name;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;



}
