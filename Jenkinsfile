pipeline {
    agent any

    environment {
        IMAGE_NAME     = "water-monitoring-ci"
        CONTAINER_NAME = "water-monitoring-ansible"
        ANSIBLE_CTR    = "ansible-docker-lab"
    }

    stages {

        // ── Stage 1: Checkout ──────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '======================================================'
                echo ' STAGE 1 - Checkout: Fetching latest source code'
                echo '======================================================'
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        // ── Stage 2: Build ─────────────────────────────────────────────────
        stage('Build') {
            steps {
                echo '======================================================'
                echo ' STAGE 2 - Build: Building Docker image'
                echo '======================================================'
                sh "docker build -t ${IMAGE_NAME} ."
                echo "Docker image '${IMAGE_NAME}' built successfully."
            }
        }

        // ── Stage 3: Test ──────────────────────────────────────────────────
        stage('Test') {
            steps {
                echo '======================================================'
                echo ' STAGE 3 - Test: Running Pytest inside Docker'
                echo '======================================================'
                // Tests run in an isolated container with a temporary database.
                // --rm removes the test container automatically after tests complete.
                // No production volume is mounted during testing.
                sh "docker run --rm ${IMAGE_NAME} python -m pytest test_app.py -v"
                echo 'All Pytest tests passed successfully.'
            }
        }

        // ── Stage 4: Deploy with Ansible ───────────────────────────────────
        stage('Deploy with Ansible') {
            steps {
                echo '======================================================'
                echo ' STAGE 4 - Deploy: Copying playbook and running Ansible'
                echo '======================================================'
                // Copy the latest playbook into the Ansible container before deploying
                sh "docker cp ansible/water-deploy.yml ${ANSIBLE_CTR}:/water-deploy.yml"
                // Run the Ansible playbook inside the ansible-docker-lab container
                sh """
                    docker exec ${ANSIBLE_CTR} ansible-playbook \
                        -i /inventory.ini \
                        /water-deploy.yml
                """
                echo 'Ansible deployment completed successfully.'
                echo 'Application is accessible at http://localhost:5002'
            }
        }
    }

    // ── Post-build actions ─────────────────────────────────────────────────
    post {
        success {
            echo '======================================================'
            echo 'SUCCESS: Smart Water Monitoring and Complaint Management CI/CD Pipeline Completed Successfully!'
            echo '======================================================'
        }
        failure {
            echo '======================================================'
            echo 'FAILURE: Smart Water Monitoring and Complaint Management CI/CD Pipeline Failed!'
            echo 'Check the stage logs above for the exact error.'
            echo '======================================================'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
