package com.closesclothes.closeclothes

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.ImageView
import android.widget.ListView
import org.json.JSONArray
import org.json.JSONObject

class CatalogActivity : AppCompatActivity() {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_catalog)
        var lvClothes = findViewById<ListView>(R.id.lvClothes)
        var clothesJson = this.clothesJsonToListOfJsons(getIntent().getStringExtra("clothesJson"))
        var adapter = ClothesListAdapter(this, R.layout.clothes_list_item, clothesJson);
        lvClothes.adapter = adapter
        lvClothes.deferNotifyDataSetChanged()

    }

    private fun clothesJsonToListOfJsons(stringExtra: String?): List<String>{
        val clothesJsons = mutableListOf<String>()
        val clothesJsonArray = JSONArray(stringExtra)
        for(i in 0..(clothesJsonArray.length()-1)){
            clothesJsons.add(clothesJsonArray.getJSONObject(i).toString())
        }
        return clothesJsons
    }
}
