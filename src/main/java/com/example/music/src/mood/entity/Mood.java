package com.example.music.src.mood.entity;

import javax.persistence.*;

@Entity
public class Mood {

    @Id @GeneratedValue
    @Column(name = "mood_id")
    private Long id;

    @Column(name = "mood_name")
    private String name;

}
