package com.example.researchapp;

import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.Bitmap.CompressFormat;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.DisplayMetrics;
import android.view.View;
import android.widget.ImageButton;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.researchapp.models.Size;
import com.otaliastudios.cameraview.CameraListener;
import com.otaliastudios.cameraview.CameraView;
import com.otaliastudios.cameraview.PictureResult;
import com.otaliastudios.cameraview.frame.Frame;
import com.otaliastudios.cameraview.frame.FrameProcessor;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    com.example.researchapp.FaceDetector faceDetector;
    CameraView camera;
    Boolean backCamera;
    static TextView textView;
    static TextView hold;
    Matrix m;
    String currentDist;
    Boolean timer;
    Boolean ready;
    Boolean flipBM;
    View top;
    View bottom;
    RelativeLayout.LayoutParams tParams;
    RelativeLayout.LayoutParams bParams;
    RelativeLayout loading;
    Integer counter;
    String[] names;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        com.example.researchapp.FaceBoundsOverlay fbo = findViewById(R.id.faceDetection);
        faceDetector = new FaceDetector(fbo);
        textView=findViewById(R.id.tv);
        hold=findViewById(R.id.hold);
        timer = false;
        m=new Matrix();
        m.postRotate(-90);
        ImageButton button = findViewById(R.id.button);
        top = findViewById(R.id.top);
        bottom = findViewById(R.id.bottom);
        loading=findViewById(R.id.loading);
        ready=true;
        flipBM=false;
        counter=0;
        names= new String[]{"cf", "mf","ff","cb","mb","fb"};

        tParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.MATCH_PARENT,
                RelativeLayout.LayoutParams.MATCH_PARENT);
        bParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.MATCH_PARENT,
                RelativeLayout.LayoutParams.MATCH_PARENT);
        tParams.height=convertDpToPixel(2);
        bParams.height=convertDpToPixel(2);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                camera.takePicture();
            }
        });
        setupCamera();

        handleDist();
    }

    void handleDist()
    {
        Thread th = new Thread(new Runnable() {
        @Override
        public void run() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    loading.setVisibility(View.INVISIBLE);
                }
            });
            handler(1400,1500,10);
            while(!ready);
            handler(1150,1250,50);
            while(!ready);
            handler(900,1000,100);
            while(!ready);
            /*runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if(!start)
                        loading.setVisibility(View.VISIBLE);
                }
            });*/
            backCamera=Boolean.TRUE;
            flipBM=true;
            camera.toggleFacing();
            handler(750,850,150);
            while(!ready);
            handler(450,550,200);
            while(!ready);
            handler(200,300,250);
            while(!ready);
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    finish();
                }
            });

        }
        synchronized void handler(Integer close, Integer far, final Integer margin)
        {
            Boolean backup=false;
            Boolean moveup=false;
            ready=false;
            currentDist=names[counter];
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    tParams.setMargins(0,convertDpToPixel(margin),0,0);
                    top.setLayoutParams(tParams);
                    bParams.setMargins(0,0,0,convertDpToPixel(margin));
                    bParams.addRule(RelativeLayout.ABOVE,R.id.filler2);
                    bottom.setLayoutParams(bParams);
                }
            });
            while(!ready)
            {
                if(textView.getText().toString() != "" &&
                        (Integer.parseInt(textView.getText().toString()) > close &&
                                Integer.parseInt(textView.getText().toString()) < far))
                {
                    camera.takePicture();
                    backup=false;
                    moveup=false;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            hold.setText("");
                        }
                    });
                    break;
                }
                else if (textView.getText().toString() != "" &&
                        Integer.parseInt(textView.getText().toString()) >= far)
                {
                    if(!backup)
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                hold.setText("Move slowly away from camera");
                            }
                        });
                    backup=true;
                    moveup=false;
                }
                else if (textView.getText().toString() != "" &&
                        Integer.parseInt(textView.getText().toString()) <= close)
                {
                    if(!moveup)
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                hold.setText("Move slowly towards the camera");
                            }
                        });
                    backup=false;
                    moveup=true;
                }
            }
        }
    });
        th.start();
    }

    void setupCamera()
    {
        camera = findViewById(R.id.camera);
        camera.toggleFacing();
        camera.setLifecycleOwner(this);
        backCamera=Boolean.FALSE;

        addFrameProcessor();

        camera.addCameraListener(new CameraListener() {
            @Override
            public void onPictureTaken(@NonNull PictureResult result) {
                super.onPictureTaken(result);
                byte[] data=result.getData();
                Bitmap bm = BitmapFactory.decodeByteArray(data, 0, data.length, null);

                File folder = new File(Environment.getExternalStorageDirectory()
                        .getAbsolutePath() +"/DCIM/research/");
                if(!folder.exists())
                    folder.mkdirs();

                try {
                    FileOutputStream out = new FileOutputStream(
                            Environment.getExternalStorageDirectory().getAbsolutePath()
                                    +"/DCIM/research/"+currentDist+".jpg");
                    if(flipBM)
                    {
                        m.preScale(-1,1);
                        System.out.println("test");
                        flipBM=false;
                    }
                    bm=Bitmap.createBitmap(bm,0,0,bm.getWidth(),bm.getHeight(),m,true);
                    bm.compress(CompressFormat.JPEG, 100, out);
                    out.close();
                    File f = new File(folder.getAbsolutePath()+"/"+currentDist+".jpg");
                    Uri uri = Uri.fromFile(f);
                    Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE,uri);
                    mediaScanIntent.setData(uri);
                    sendBroadcast(mediaScanIntent);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                camera.close();
                camera.open();
                counter++;
                ready=true;
            }
        });
    }

    void addFrameProcessor()
    {
        camera.addFrameProcessor(new FrameProcessor() {
            @Override
            public void process(@NonNull Frame frame) {
                faceDetector.process(
                        new com.example.researchapp.models.Frame(
                                (byte[])frame.getData(),
                                frame.getRotation(),
                                new Size(frame.getSize().getWidth(),frame.getSize().getHeight()),
                                frame.getFormat(),
                                backCamera));

            }
        });
    }

    public int convertDpToPixel(float dp) {
        Context context = getApplicationContext();
        if (context == null) {
            return 0; // context should never be a null
        }
        Resources resources = context.getResources();
        DisplayMetrics metrics = resources.getDisplayMetrics();
        return (int) (dp * ((float) metrics.densityDpi / DisplayMetrics.DENSITY_DEFAULT));
    }
}