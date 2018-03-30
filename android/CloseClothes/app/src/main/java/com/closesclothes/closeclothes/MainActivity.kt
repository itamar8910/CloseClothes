package com.closesclothes.closeclothes

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.view.View

class MainActivity : AppCompatActivity() {

    public val TAG : String = "CloseClothes"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)



    }



    fun BCameraClick(view : View?){
        startActivity( Intent(this, CameraActivity::class.java));
    }
}
