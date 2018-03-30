package com.closesclothes.closeclothes

import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import android.widget.ImageView
import android.widget.Toast
import com.closesclothes.closeclothes.utils.SocketWrapper
import java.io.ByteArrayOutputStream
import kotlin.concurrent.thread
import android.os.Environment.getExternalStorageDirectory
import android.os.Environment.getExternalStorageDirectory
import android.view.View
import java.io.File
import android.os.StrictMode
import android.os.Build
import java.text.SimpleDateFormat
import java.util.*
import android.graphics.BitmapFactory




class CameraActivity : AppCompatActivity() {

    private val REQUEST_IMAGE_CAPTURE = 1

    private var imPic : ImageView? = null;
    var CAMERA_PIC_REQUEST = 2

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_camera)
        if (Build.VERSION.SDK_INT >= 24) {
            try {
                val m = StrictMode::class.java.getMethod("disableDeathOnFileUriExposure")
                m.invoke(null)
            } catch (e: Exception) {
                e.printStackTrace()
            }

        }
        imPic = findViewById<ImageView>(R.id.imPic);


        dispatchTakePictureIntent();

    }


    private var pictureImagePath: String = "";

    private fun dispatchTakePictureIntent() {
        val timeStamp = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val imageFileName = timeStamp + ".jpg"
        val storageDir = Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES)
        pictureImagePath = storageDir.absolutePath + "/" + imageFileName
        val file = File(pictureImagePath)
        val outputFileUri = Uri.fromFile(file)
        val cameraIntent = Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE)
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, outputFileUri)
        startActivityForResult(cameraIntent, 1)
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode === 1) {
            val imgFile = File(pictureImagePath)
            if (imgFile.exists()) {
                val myBitmap = BitmapFactory.decodeFile(imgFile.absolutePath)
                imPic?.setImageBitmap(myBitmap)
                Toast.makeText(this@CameraActivity, myBitmap.width.toString() + "," + myBitmap.height.toString(), Toast.LENGTH_SHORT).show();
                //bitmap size: 189,252
                sendImageToServer(myBitmap)
            }
        }
    }

    private fun sendImageToServer(imageBitmap: Bitmap) {
        thread(){
            var correctSize = Bitmap.createScaledBitmap(imageBitmap, 150, 150, false);
            var stream = ByteArrayOutputStream()
            imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
            var byteArray = stream.toByteArray()
            val socketWrapper = SocketWrapper()
            Log.i(MainActivity::TAG.toString(), "image bytes size:" + byteArray.size)
            socketWrapper.send(socketWrapper.intToByteArray(byteArray.size))
            socketWrapper.send(byteArray)
            var resultJson = socketWrapper.receiveJson()
            Log.i(MainActivity::TAG.toString(), "result JSON:" + resultJson.toString())
            socketWrapper.closeSocket()
        }

    }

}
