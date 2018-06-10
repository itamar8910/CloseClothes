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
import android.widget.EditText
import com.closesclothes.closeclothes.R.id.etIP


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
        intent = Intent(this, CameraActivity::class.java)
        var etIP = findViewById<EditText>(R.id.etIP);
        intent.putExtra("ip", etIP.text.toString())
        startActivity( intent);
//        startActivity( Intent(this, CatalogActivity::class.java));
    }

    // dummy method to test clothes list with dummy data
    fun bTestClothesListClick(view : View?){
        val clothesJson = "[{\"url\": \"https://www.castro.com/he/MEN/T-shirts/Asymmetrical-tee-322232.html\", \"imgs\": [\"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170651.01.2200_5f90b55.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170651.01.2200_d_410c25c.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170651.01.2200_d1_f3f83f2.jpg\"], \"description\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea \\\\u05d8\\\\u05d9 \\\\u05e2\\\\u05dd \\\\u05d7\\\\u05ea\\\\u05db\\\\u05d9\\\\u05dd \\\\u05d5\\\\u05de\\\\u05db\\\\u05e4\\\\u05dc\\\\u05ea \\\\u05d0-\\\\u05e1\\\\u05d9\\\\u05de\\\\u05d8\\\\u05e8\\\\u05d9\\\\u05ea \\\\u05d1\\\\u05de\\\\u05e8\\\\u05d0\\\\u05d4 \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05dd\\n\\n\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05d0\\\\u05e8\\\\u05d5\\\\u05df \\\\u05e2\\\\u05d2\\\\u05d5\\\\u05dc \\\\u05d1\\\\u05de\\\\u05e8\\\\u05d0\\\\u05d4 \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05dd\\n\\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc\\\\u05d9\\\\u05dd \\\\u05e7\\\\u05e6\\\\u05e8\\\\u05d9\\\\u05dd\\n\\\\u05d2\\\\u05d5\\\\u05d1\\\\u05d4 \\\\u05d4\\\\u05d3\\\\u05d5\\\\u05d2\\\\u05de\\\\u05df 1.89, \\\\u05dc\\\\u05d5\\\\u05d1\\\\u05e9 \\\\u05de\\\\u05d9\\\\u05d3\\\\u05d4 L\\n\\\\u05de\\\\u05ea\\\\u05d5\\\\u05da \\\\u05e7\\\\u05d5\\\\u05dc\\\\u05e7\\\\u05e6\\\\u05d9\\\\u05d9\\\\u05ea RED, \\\\u05e7\\\\u05d5 \\\\u05d0\\\\u05d5\\\\u05e4\\\\u05e0\\\\u05ea \\\\u05d4\\\\u05e7\\\\u05d6'\\\\u05d5\\\\u05d0\\\\u05dc \\\\u05e9\\\\u05dc \\\\u05e7\\\\u05e1\\\\u05d8\\\\u05e8\\\\u05d5\", \"sizes\": [\"XS\", \"S\", \"M\", \"L\"], \"color\": \"\\\\u05ea\\\\u05db\\\\u05dc\\\\u05ea\", \"gender\": \"Male\", \"price\": \"79.90[NIS]\", \"brand\": \"Castro\", \"name\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea \\\\u05d8\\\\u05d9 \\\\u05d0-\\\\u05e1\\\\u05d9\\\\u05de\\\\u05d8\\\\u05e8\\\\u05d9\\\\u05ea\"}, {\"url\": \"https://www.castro.com/he/MEN/T-shirts/Sleeveless-shirt-325062.html\", \"description\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05d4 \\\\u05dc\\\\u05dc\\\\u05d0 \\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc\\\\u05d9\\\\u05dd \\\\u05e2\\\\u05dd \\\\u05e7\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05ea \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05de\\\\u05d9\\\\u05dd\\n\\n\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05d0\\\\u05e8\\\\u05d5\\\\u05df  \\\\u05e2\\\\u05d2\\\\u05d5\\\\u05dc\\n\\\\u05e4\\\\u05ea\\\\u05d7\\\\u05d9 \\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc \\\\u05e8\\\\u05d7\\\\u05d1\\\\u05d9\\\\u05dd\\n\\\\u05d2\\\\u05d5\\\\u05d1\\\\u05d4 \\\\u05d4\\\\u05d3\\\\u05d5\\\\u05d2\\\\u05de\\\\u05df 1.88, \\\\u05dc\\\\u05d5\\\\u05d1\\\\u05e9 \\\\u05de\\\\u05d9\\\\u05d3\\\\u05d4 L\\n\\\\u05de\\\\u05ea\\\\u05d5\\\\u05da \\\\u05e7\\\\u05d5\\\\u05dc\\\\u05e7\\\\u05e6\\\\u05d9\\\\u05d9\\\\u05ea RED, \\\\u05e7\\\\u05d5 \\\\u05d0\\\\u05d5\\\\u05e4\\\\u05e0\\\\u05ea \\\\u05d4\\\\u05e7\\\\u05d6'\\\\u05d5\\\\u05d0\\\\u05dc \\\\u05e9\\\\u05dc \\\\u05e7\\\\u05e1\\\\u05d8\\\\u05e8\\\\u05d5\", \"sizes\": [\"XS\", \"S\", \"M\", \"L\", \"XL\"], \"imgs\": [\"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/0/7070064.01.2100_6a12991.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/0/7070064.01.2100_d_1b9a481.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/0/7070064.01.2100_d1_7d2a045.jpg\"], \"gender\": \"Male\", \"price\": \"49.90[NIS]\", \"brand\": \"Castro\", \"color\": \"\\\\u05e0\\\\u05d9\\\\u05d9\\\\u05d1\\\\u05d9\", \"name\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea sleeveles\"}, {\"url\": \"https://www.castro.com/he/MEN/T-shirts/Deep-V-T-shirt-322150.html\", \"imgs\": [\"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170656.01.3700_a39f69b.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170656.01.3700_d_8b59be2.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170656.01.3700_d1_c4ed058.jpg\"], \"description\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea \\\\u05d8\\\\u05d9 \\\\u05e2\\\\u05dd \\\\u05e6\\\\u05d5\\\\u05d5\\\\u05d0\\\\u05e8\\\\u05d5\\\\u05df \\\\u05d5\\\\u05d9 \\\\u05e2\\\\u05de\\\\u05d5\\\\u05e7 \\\\u05d1\\\\u05de\\\\u05e8\\\\u05d0\\\\u05d4 \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05dd\\n\\n\\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc\\\\u05d9\\\\u05dd \\\\u05e7\\\\u05e6\\\\u05e8\\\\u05d9\\\\u05dd\\n\\\\u05d2\\\\u05d5\\\\u05d1\\\\u05d4 \\\\u05d4\\\\u05d3\\\\u05d5\\\\u05d2\\\\u05de\\\\u05df 1.89, \\\\u05dc\\\\u05d5\\\\u05d1\\\\u05e9 \\\\u05de\\\\u05d9\\\\u05d3\\\\u05d4 L\\n\\\\u05de\\\\u05ea\\\\u05d5\\\\u05da \\\\u05e7\\\\u05d5\\\\u05dc\\\\u05e7\\\\u05e6\\\\u05d9\\\\u05d9\\\\u05ea RED, \\\\u05e7\\\\u05d5 \\\\u05d0\\\\u05d5\\\\u05e4\\\\u05e0\\\\u05ea \\\\u05d4\\\\u05e7\\\\u05d6'\\\\u05d5\\\\u05d0\\\\u05dc \\\\u05e9\\\\u05dc \\\\u05e7\\\\u05e1\\\\u05d8\\\\u05e8\\\\u05d5\", \"sizes\": [\"XS\", \"S\", \"M\", \"L\", \"XL\", \"XXL\"], \"color\": \"\\\\u05d7\\\\u05d0\\\\u05e7\\\\u05d9\", \"gender\": \"Male\", \"price\": \"59.90[NIS]\", \"brand\": \"Castro\", \"name\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea \\\\u05d8\\\\u05d9 \\\\u05d5\\\\u05d9 \\\\u05e2\\\\u05de\\\\u05d5\\\\u05e7\"}, {\"url\": \"https://www.castro.com/he/MEN/T-shirts/Sleeveless-top-with-raw-edge-317662.html\", \"description\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05d4 \\\\u05dc\\\\u05dc\\\\u05d0 \\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc\\\\u05d9\\\\u05dd \\\\u05e2\\\\u05dd \\\\u05e7\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05ea \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05de\\\\u05d9\\\\u05dd\\n\\n\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05d0\\\\u05e8\\\\u05d5\\\\u05df  \\\\u05e2\\\\u05d2\\\\u05d5\\\\u05dc\\n\\\\u05e4\\\\u05ea\\\\u05d7\\\\u05d9 \\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc \\\\u05e8\\\\u05d7\\\\u05d1\\\\u05d9\\\\u05dd\\n\\\\u05d2\\\\u05d5\\\\u05d1\\\\u05d4 \\\\u05d4\\\\u05d3\\\\u05d5\\\\u05d2\\\\u05de\\\\u05df 1.84, \\\\u05dc\\\\u05d5\\\\u05d1\\\\u05e9 \\\\u05de\\\\u05d9\\\\u05d3\\\\u05d4 L\\n\\\\u05de\\\\u05ea\\\\u05d5\\\\u05da \\\\u05e7\\\\u05d5\\\\u05dc\\\\u05e7\\\\u05e6\\\\u05d9\\\\u05d9\\\\u05ea RED, \\\\u05e7\\\\u05d5 \\\\u05d0\\\\u05d5\\\\u05e4\\\\u05e0\\\\u05ea \\\\u05d4\\\\u05e7\\\\u05d6'\\\\u05d5\\\\u05d0\\\\u05dc \\\\u05e9\\\\u05dc \\\\u05e7\\\\u05e1\\\\u05d8\\\\u05e8\\\\u05d5\", \"sizes\": [\"XS\", \"S\",\"M\", \"L\", \"XXL\"], \"imgs\": [\"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/0/7070066.01.2100_59462fa.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/0/7070066.01.2100_d_b394d17.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/0/7070066.01.2100_d1_969a060.jpg\"], \"gender\": \"Male\", \"price\": \"59.90[NIS]\", \"brand\": \"Castro\", \"color\": \"\\\\u05e0\\\\u05d9\\\\u05d9\\\\u05d1\\\\u05d9\", \"name\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea sleeveles \\\\u05e2\\\\u05dd \\\\u05e7\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05ea \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05de\\\\u05d9\\\\u05dd\"}, {\"url\": \"https://www.castro.com/he/MEN/T-shirts/Raw-edge-T-shirt-315334.html\", \"imgs\": [\"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170668.01.1062_0581255.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170668.01.1062_d_e8d64f2.jpg\", \"https://d356cpcjxoolwe.cloudfront.net/media/catalog/product/cache/3/image/373x485/72b4a3c89279b6295f5413414e9ad668/7/1/7170668.01.1062_d1_612e98b.jpg\"], \"description\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea \\\\u05d8\\\\u05d9 \\\\u05e2\\\\u05dd \\\\u05d2\\\\u05d9\\\\u05de\\\\u05d5\\\\u05e8\\\\u05d9\\\\u05dd \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05de\\\\u05d9\\\\u05dd\\n\\n\\\\u05e6\\\\u05d5\\\\u05d5\\\\u05d0\\\\u05e8\\\\u05d5\\\\u05df \\\\u05e2\\\\u05d2\\\\u05d5\\\\u05dc\\n\\\\u05e9\\\\u05e8\\\\u05d5\\\\u05d5\\\\u05dc\\\\u05d9\\\\u05dd \\\\u05e7\\\\u05e6\\\\u05e8\\\\u05d9\\\\u05dd \\\\u05de\\\\u05e7\\\\u05d5\\\\u05e4\\\\u05dc\\\\u05d9\\\\u05dd\\n\\\\u05d2\\\\u05d5\\\\u05d1\\\\u05d4 \\\\u05d4\\\\u05d3\\\\u05d5\\\\u05d2\\\\u05de\\\\u05df 1.88, \\\\u05dc\\\\u05d5\\\\u05d1\\\\u05e9 \\\\u05de\\\\u05d9\\\\u05d3\\\\u05d4 L\\n\\\\u05de\\\\u05ea\\\\u05d5\\\\u05da \\\\u05e7\\\\u05d5\\\\u05dc\\\\u05e7\\\\u05e6\\\\u05d9\\\\u05d9\\\\u05ea RED, \\\\u05e7\\\\u05d5 \\\\u05d0\\\\u05d5\\\\u05e4\\\\u05e0\\\\u05ea \\\\u05d4\\\\u05e7\\\\u05d6'\\\\u05d5\\\\u05d0\\\\u05dc \\\\u05e9\\\\u05dc \\\\u05e7\\\\u05e1\\\\u05d8\\\\u05e8\\\\u05d5\", \"sizes\": [\"XS\", \"S\", \"M\", \"L\", \"XL\"], \"color\": \"\\\\u05d0\\\\u05d1\\\\u05df\", \"gender\": \"Male\", \"price\": \"59.90[NIS]\", \"brand\": \"Castro\", \"name\": \"\\\\u05d7\\\\u05d5\\\\u05dc\\\\u05e6\\\\u05ea \\\\u05d8\\\\u05d9 \\\\u05d2\\\\u05d9\\\\u05de\\\\u05d5\\\\u05e8\\\\u05d9\\\\u05dd \\\\u05e4\\\\u05e8\\\\u05d5\\\\u05de\\\\u05d9\\\\u05dd\"}]"
        var intent = Intent(this, CatalogActivity::class.java)
        intent.putExtra("clothesJson", clothesJson)
        startActivity(intent)
    }
}
