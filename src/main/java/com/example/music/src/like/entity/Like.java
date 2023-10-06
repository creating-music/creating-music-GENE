package com.example.music.src.like.entity;

import lombok.Getter;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Getter
@Entity
@Table(name = "Like")
public class Like {

    @Id @GeneratedValue
    private Long id;

    private String

}
