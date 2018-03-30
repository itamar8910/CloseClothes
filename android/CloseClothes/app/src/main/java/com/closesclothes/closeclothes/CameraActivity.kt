package com.closesclothes.closeclothes

import android.content.Intent
import android.graphics.Bitmap
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.widget.ImageView
import android.widget.Toast
import com.closesclothes.closeclothes.utils.SocketWrapper
import java.io.ByteArrayOutputStream
import kotlin.concurrent.thread

class CameraActivity : AppCompatActivity() {

    private val REQUEST_IMAGE_CAPTURE = 1

    private var imPic : ImageView? = null;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_camera)

        imPic = findViewById<ImageView>(R.id.imPic);


        dispatchTakePictureIntent();

    }


    private fun dispatchTakePictureIntent() {
        val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        if (takePictureIntent.resolveActivity(packageManager) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE)
        }
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            val extras = data.extras
            val imageBitmap = extras.get("data") as Bitmap
            imPic?.setImageBitmap(imageBitmap)
            Toast.makeText(this@CameraActivity, imageBitmap.width.toString() + "," + imageBitmap.height.toString(), Toast.LENGTH_SHORT).show();
            //bitmap size: 189,252
            sendImageToServer(imageBitmap)
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
