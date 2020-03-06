package com.example.researchapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import com.otaliastudios.cameraview.CameraView;
import com.otaliastudios.cameraview.frame.Frame;
import com.otaliastudios.cameraview.frame.FrameProcessor;

import husaynhakeem.io.facedetector.FaceBoundsOverlay;
import husaynhakeem.io.facedetector.FaceDetector;
import husaynhakeem.io.facedetector.models.Size;

public class MainActivity extends AppCompatActivity {

    FaceDetector faceDetector;
    CameraView camera;
    Boolean front;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        FaceBoundsOverlay fbo = findViewById(R.id.faceDetection);
        faceDetector = new FaceDetector(fbo);

        setupCamera();
    }

    void setupCamera()
    {
        camera = findViewById(R.id.camera);
        camera.toggleFacing();
        camera.setLifecycleOwner(this);
        front=Boolean.TRUE;
        camera.addFrameProcessor(new FrameProcessor() {
            @Override
            public void process(@NonNull Frame frame) {
                faceDetector.process(
                        new husaynhakeem.io.facedetector.models.Frame(
                                (byte[])frame.getData(),
                                frame.getRotation(),
                                new Size(frame.getSize().getWidth(),frame.getSize().getHeight()),
                                frame.getFormat(),
                                front));

            }
        });
    }
}