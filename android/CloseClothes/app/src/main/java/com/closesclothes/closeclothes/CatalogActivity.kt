package com.closesclothes.closeclothes

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.ImageView
import android.widget.ListView

class CatalogActivity : AppCompatActivity() {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_catalog)
        var lvClothes = findViewById<ListView>(R.id.lvClothes)

        var adapter = ClothesListAdapter(this, R.layout.clothes_list_item, listOf("a", "b"));
        lvClothes.adapter = adapter
        lvClothes.deferNotifyDataSetChanged()

    }
}
