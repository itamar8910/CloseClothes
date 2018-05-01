package com.closesclothes.closeclothes

import android.Manifest
import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.support.v4.app.ActivityCompat.requestPermissions
import android.Manifest.permission
import android.Manifest.permission.WRITE_EXTERNAL_STORAGE
import android.Manifest.permission.READ_EXTERNAL_STORAGE
import android.app.PendingIntent.getActivity
import android.os.Build
import android.support.v4.app.ActivityCompat
import android.content.pm.PackageManager
import android.support.v4.content.ContextCompat




class MainActivity : AppCompatActivity() {

    public val TAG : String = "CloseClothes"


    private val MY_PERMISSIONS_REQUEST_READ_CONTACTS: Int = 1;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.READ_CONTACTS)
                != PackageManager.PERMISSION_GRANTED) {


            ActivityCompat.requestPermissions(this,
                    arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE),
                    MY_PERMISSIONS_REQUEST_READ_CONTACTS)
            //TODO: check permission result
        }
    }


    fun BCameraClick(view : View?){
        startActivity( Intent(this, CameraActivity::class.java));
//        startActivity( Intent(this, CatalogActivity::class.java));
    }
}
