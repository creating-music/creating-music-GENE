package com.example.music.src.music.entity;

import javax.persistence.*;

@Entity
public class Genre {

    @Id @GeneratedValue
    @Column(name = "genre_id")
    private Long id;

    @Column(name = "genre_name")
    private String name;
}
