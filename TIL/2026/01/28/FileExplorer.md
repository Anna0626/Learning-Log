# FileExplorer

> 날짜: 2026-01-28
> 원본 노션: [링크](https://www.notion.so/FileExplorer-2f7b28703eb080e2842ecdad9a0bbbfc)

---

```java
package gui;

import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Cursor;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.BorderFactory;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.JTree;
import javax.swing.ListSelectionModel;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import javax.swing.event.TreeExpansionEvent;
import javax.swing.event.TreeExpansionListener;
import javax.swing.filechooser.FileSystemView;
import javax.swing.table.DefaultTableModel;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreePath;

public class FileExplorer extends JFrame {
    private JTree tree;
    private JTable table;
    private DefaultTableModel tableModel;
    private JSplitPane splitPane;
    private JTextField pathField;
    private File currentDirectory;
    private JPanel fileDisplayPanel;
    private CardLayout cardLayout;
    private JPanel iconPanel;
    private static final String TABLE_VIEW = "table";
    private static final String ICON_VIEW = "icon";
    private FileSystemView fileSystemView;
    
    public FileExplorer() {
        setTitle("파일 탐색기");
        setSize(1000, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        
        // FileSystemView 초기화
        fileSystemView = FileSystemView.getFileSystemView();
        
        // 레이아웃 설정
        setLayout(new BorderLayout());
        
        // 상단 툴바 추가
        JPanel topPanel = createTopPanel();
        add(topPanel, BorderLayout.NORTH);
        
        // 왼쪽 패널 - 트리 구조
        JPanel leftPanel = createTreePanel();
        
        // 오른쪽 패널 - 파일 목록 테이블
        JPanel rightPanel = createTablePanel();
        
        // SplitPane으로 나누기
        splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, leftPanel, rightPanel);
        splitPane.setDividerLocation(300);
        splitPane.setOneTouchExpandable(true);
        
        add(splitPane, BorderLayout.CENTER);
        
        // 상태 표시줄
        JLabel statusBar = new JLabel(" 준비");
        statusBar.setBorder(BorderFactory.createEtchedBorder());
        add(statusBar, BorderLayout.SOUTH);
    }
    
    // 상단 패널 생성 (경로 입력 + 보기 스타일 버튼)
    private JPanel createTopPanel() {
        JPanel panel = new JPanel(new BorderLayout(5, 5));
        panel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
        
        // 경로 입력 패널
        JPanel pathPanel = new JPanel(new BorderLayout(5, 0));
        JLabel pathLabel = new JLabel("경로:");
        pathField = new JTextField();
        pathField.setFont(new Font("Dialog", Font.PLAIN, 12));
        
        // 경로 입력 후 엔터키 이벤트
        pathField.addActionListener(e -> {
            String path = pathField.getText().trim();
            if (!path.isEmpty()) {
                File newDir = new File(path);
                if (newDir.exists() && newDir.isDirectory()) {
                    navigateToDirectory(newDir);
                } else {
                    JOptionPane.showMessageDialog(
                        this,
                        "유효하지 않은 경로입니다.",
                        "오류",
                        JOptionPane.ERROR_MESSAGE
                    );
                }
            }
        });
        
        JButton goButton = new JButton("이동");
        goButton.addActionListener(e -> {
            String path = pathField.getText().trim();
            if (!path.isEmpty()) {
                File newDir = new File(path);
                if (newDir.exists() && newDir.isDirectory()) {
                    navigateToDirectory(newDir);
                } else {
                    JOptionPane.showMessageDialog(
                        this,
                        "유효하지 않은 경로입니다.",
                        "오류",
                        JOptionPane.ERROR_MESSAGE
                    );
                }
            }
        });
        
        pathPanel.add(pathLabel, BorderLayout.WEST);
        pathPanel.add(pathField, BorderLayout.CENTER);
        pathPanel.add(goButton, BorderLayout.EAST);
        
        // 보기 스타일 버튼 패널
        JPanel viewPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 5, 0));
        
        JButton tableViewButton = new JButton("목록");
        tableViewButton.setToolTipText("목록으로 보기");
        tableViewButton.setFocusPainted(false);
        
        JButton iconViewButton = new JButton("아이콘");
        iconViewButton.setToolTipText("아이콘으로 보기");
        iconViewButton.setFocusPainted(false);
        
        tableViewButton.addActionListener(e -> {
            cardLayout.show(fileDisplayPanel, TABLE_VIEW);
        });
        
        iconViewButton.addActionListener(e -> {
            cardLayout.show(fileDisplayPanel, ICON_VIEW);
            updateIconView(currentDirectory);
        });
        
        viewPanel.add(new JLabel("보기:"));
        viewPanel.add(tableViewButton);
        viewPanel.add(iconViewButton);
        
        panel.add(pathPanel, BorderLayout.CENTER);
        panel.add(viewPanel, BorderLayout.EAST);
        
        return panel;
    }
    
    // 트리 패널 생성
    private JPanel createTreePanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("폴더 구조"));
        
        // 루트 노드 생성
        DefaultMutableTreeNode root = new DefaultMutableTreeNode("내 컴퓨터");
        
        // 시스템의 루트 디렉토리들 추가
        File[] roots = File.listRoots();
        for (File fileRoot : roots) {
            DefaultMutableTreeNode node = new DefaultMutableTreeNode(fileRoot);
            root.add(node);
            // 하위 디렉토리가 있는지 확인용 더미 노드 추가
            File[] files = fileRoot.listFiles();
            if (files != null && files.length > 0) {
                node.add(new DefaultMutableTreeNode("Loading..."));
            }
        }
        
        // 트리 생성
        tree = new JTree(root);
        tree.setShowsRootHandles(true);
        
        // 커스텀 셀 렌더러 설정 - 파일명만 표시
        tree.setCellRenderer(new DefaultTreeCellRenderer() {
            @Override
            public Component getTreeCellRendererComponent(JTree tree, Object value,
                    boolean sel, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row, hasFocus);
                
                if (value instanceof DefaultMutableTreeNode) {
                    DefaultMutableTreeNode node = (DefaultMutableTreeNode) value;
                    Object userObject = node.getUserObject();
                    
                    if (userObject instanceof File) {
                        File file = (File) userObject;
                        // 루트 디렉토리인 경우 전체 경로, 아니면 파일명만 표시
                        if (file.getParent() == null) {
                            setText(file.getAbsolutePath());
                        } else {
                            setText(file.getName());
                        }
                        
                        // 시스템 아이콘 사용
                        Icon icon = fileSystemView.getSystemIcon(file);
                        setIcon(icon);
                    }
                }
                
                return this;
            }
        });
        
        // 트리 확장 이벤트 리스너
        tree.addTreeExpansionListener(new TreeExpansionListener() {
            @Override
            public void treeExpanded(TreeExpansionEvent event) {
                DefaultMutableTreeNode node = 
                    (DefaultMutableTreeNode) event.getPath().getLastPathComponent();
                loadChildren(node);
            }
            
            @Override
            public void treeCollapsed(TreeExpansionEvent event) {
                // 필요시 구현
            }
        });
        
        // 트리 선택 이벤트 리스너 - 단일 클릭으로도 파일 목록 업데이트
        tree.addTreeSelectionListener(e -> {
            DefaultMutableTreeNode node = 
                (DefaultMutableTreeNode) tree.getLastSelectedPathComponent();
            if (node != null && node.getUserObject() instanceof File) {
                File file = (File) node.getUserObject();
                if (file.isDirectory()) {
                    currentDirectory = file;
                    pathField.setText(file.getAbsolutePath());
                    updateTable(file);
                }
            }
        });
        
        JScrollPane scrollPane = new JScrollPane(tree);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    // 트리 노드의 하위 디렉토리 로드
    private void loadChildren(DefaultMutableTreeNode parent) {
        Object userObject = parent.getUserObject();
        if (!(userObject instanceof File)) return;
        
        File file = (File) userObject;
        
        // 이미 로드되었는지 확인
        if (parent.getChildCount() > 0) {
            DefaultMutableTreeNode firstChild = 
                (DefaultMutableTreeNode) parent.getFirstChild();
            if (firstChild.getUserObject() instanceof String) {
                parent.removeAllChildren();
            } else {
                return; // 이미 로드됨
            }
        }
        
        // 하위 디렉토리 로드
        File[] files = file.listFiles();
        if (files != null) {
            for (File f : files) {
                if (f.isDirectory() && !f.isHidden()) {
                    DefaultMutableTreeNode node = new DefaultMutableTreeNode(f);
                    parent.add(node);
                    
                    // 하위 디렉토리가 있는지 확인
                    File[] subFiles = f.listFiles();
                    if (subFiles != null && subFiles.length > 0) {
                        boolean hasSubDir = false;
                        for (File sf : subFiles) {
                            if (sf.isDirectory() && !sf.isHidden()) {
                                hasSubDir = true;
                                break;
                            }
                        }
                        if (hasSubDir) {
                            node.add(new DefaultMutableTreeNode("Loading..."));
                        }
                    }
                }
            }
        }
        
        // 트리 모델 업데이트
        ((DefaultTreeModel) tree.getModel()).reload(parent);
    }
    
    // 테이블 패널 생성
    private JPanel createTablePanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("파일 목록"));
        
        // CardLayout으로 테이블 뷰와 아이콘 뷰 전환
        cardLayout = new CardLayout();
        fileDisplayPanel = new JPanel(cardLayout);
        
        // 테이블 뷰 패널
        JPanel tableViewPanel = createTableViewPanel();
        
        // 아이콘 뷰 패널 - WrapLayout 사용
        iconPanel = new JPanel(new WrapLayout(FlowLayout.LEFT, 10, 10));
        iconPanel.setBackground(Color.WHITE);
        JScrollPane iconScrollPane = new JScrollPane(iconPanel);
        iconScrollPane.getVerticalScrollBar().setUnitIncrement(16);
        iconScrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        
        fileDisplayPanel.add(tableViewPanel, TABLE_VIEW);
        fileDisplayPanel.add(iconScrollPane, ICON_VIEW);
        
        panel.add(fileDisplayPanel, BorderLayout.CENTER);
        
        return panel;
    }
    
    // 테이블 뷰 패널 생성
    private JPanel createTableViewPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        
        // 테이블 모델 생성
        String[] columnNames = {"이름", "크기", "종류", "수정한 날짜"};
        tableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        
        table = new JTable(tableModel);
        table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        table.setRowHeight(20);
        
        // 컬럼 너비 설정
        table.getColumnModel().getColumn(0).setPreferredWidth(300);
        table.getColumnModel().getColumn(1).setPreferredWidth(100);
        table.getColumnModel().getColumn(2).setPreferredWidth(150);
        table.getColumnModel().getColumn(3).setPreferredWidth(200);
        
        // 단일 클릭 이벤트 - 폴더 선택 시 이동
        table.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 1) {
                    int row = table.getSelectedRow();
                    if (row >= 0) {
                        String fileName = (String) tableModel.getValueAt(row, 0);
                        String fileType = (String) tableModel.getValueAt(row, 2);
                        
                        // 위로 가기 항목 처리
                        if (fileName.equals("[위로 가기]")) {
                            File parentDir = currentDirectory.getParentFile();
                            if (parentDir != null) {
                                navigateToDirectory(parentDir);
                            }
                        } else if (fileType.equals("파일 폴더")) {
                            // 폴더 클릭 시 해당 폴더로 이동
                            File newDir = new File(currentDirectory, fileName);
                            if (newDir.exists() && newDir.isDirectory()) {
                                navigateToDirectory(newDir);
                            }
                        }
                    }
                }
            }
        });
        
        // 더블클릭 이벤트 - 파일 열기
        table.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    int row = table.getSelectedRow();
                    if (row >= 0) {
                        String fileName = (String) tableModel.getValueAt(row, 0);
                        String fileType = (String) tableModel.getValueAt(row, 2);
                        
                        // 위로 가기는 단일 클릭에서 처리
                        if (fileName.equals("[위로 가기]")) {
                            return;
                        }
                        
                        // 폴더는 단일 클릭에서 처리
                        if (fileType.equals("파일 폴더")) {
                            return;
                        }
                        
                        // 파일 더블클릭 시 열기
                        File selectedFile = new File(currentDirectory, fileName);
                        
                        if (isTextFile(selectedFile)) {
                            openTextViewer(selectedFile);
                        } else {
                            // 다른 파일 타입은 시스템 기본 프로그램으로 열기 시도
                            try {
                                if (Desktop.isDesktopSupported()) {
                                    Desktop.getDesktop().open(selectedFile);
                                }
                            } catch (Exception ex) {
                                JOptionPane.showMessageDialog(
                                    FileExplorer.this,
                                    "파일을 열 수 없습니다: " + ex.getMessage(),
                                    "오류",
                                    JOptionPane.ERROR_MESSAGE
                                );
                            }
                        }
                    }
                }
            }
        });
        
        JScrollPane scrollPane = new JScrollPane(table);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    // 테이블 업데이트
    private void updateTable(File directory) {
        tableModel.setRowCount(0);
        
        if (!directory.isDirectory()) {
            return;
        }
        
        currentDirectory = directory;
        pathField.setText(directory.getAbsolutePath());
        
        // 위로 가기 항목 추가 (부모 디렉토리가 있는 경우)
        File parentDir = directory.getParentFile();
        if (parentDir != null) {
            tableModel.addRow(new Object[]{"[위로 가기]", "", "상위 폴더", ""});
        }
        
        File[] files = directory.listFiles();
        if (files == null) {
            return;
        }
        
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        
        for (File file : files) {
            if (file.isHidden()) continue;
            
            String name = file.getName();
            String size = file.isDirectory() ? "" : formatFileSize(file.length());
            String type = file.isDirectory() ? "파일 폴더" : getFileType(file);
            String modified = sdf.format(new Date(file.lastModified()));
            
            tableModel.addRow(new Object[]{name, size, type, modified});
        }
        
        // 아이콘 뷰도 함께 업데이트
        updateIconView(directory);
    }
    
    // 파일 크기 포맷
    private String formatFileSize(long size) {
        if (size < 1024) {
            return size + " B";
        } else if (size < 1024 * 1024) {
            return String.format("%.2f KB", size / 1024.0);
        } else if (size < 1024 * 1024 * 1024) {
            return String.format("%.2f MB", size / (1024.0 * 1024));
        } else {
            return String.format("%.2f GB", size / (1024.0 * 1024 * 1024));
        }
    }
    
    // 파일 타입 가져오기
    private String getFileType(File file) {
        String name = file.getName();
        int dotIndex = name.lastIndexOf('.');
        
        if (dotIndex > 0 && dotIndex < name.length() - 1) {
            String extension = name.substring(dotIndex + 1).toUpperCase();
            return extension + " 파일";
        }
        
        return "파일";
    }
    
    // 텍스트 파일인지 확인
    private boolean isTextFile(File file) {
        String name = file.getName().toLowerCase();
        String[] textExtensions = {".txt", ".log", ".java", ".xml", ".html", 
                                   ".css", ".js", ".json", ".md", ".csv", 
                                   ".properties", ".ini", ".cfg", ".conf"};
        
        for (String ext : textExtensions) {
            if (name.endsWith(ext)) {
                return true;
            }
        }
        return false;
    }
    
    // 아이콘 뷰 업데이트
    private void updateIconView(File directory) {
        iconPanel.removeAll();
        
        if (directory == null || !directory.isDirectory()) {
            iconPanel.revalidate();
            iconPanel.repaint();
            return;
        }
        
        // 위로 가기 항목 추가 (부모 디렉토리가 있는 경우)
        File parentDir = directory.getParentFile();
        if (parentDir != null) {
            JPanel upPanel = createUpNavigationPanel(parentDir);
            iconPanel.add(upPanel);
        }
        
        File[] files = directory.listFiles();
        if (files == null) {
            iconPanel.revalidate();
            iconPanel.repaint();
            return;
        }
        
        for (File file : files) {
            if (file.isHidden()) continue;
            
            JPanel fileIconPanel = createFileIconPanel(file);
            iconPanel.add(fileIconPanel);
        }
        
        iconPanel.revalidate();
        iconPanel.repaint();
    }
    
    // 위로 가기 패널 생성
    private JPanel createUpNavigationPanel(File parentDir) {
        JPanel upPanel = new JPanel();
        upPanel.setLayout(new BorderLayout(5, 5));
        upPanel.setPreferredSize(new Dimension(100, 120));
        upPanel.setBackground(new Color(255, 255, 220));
        upPanel.setBorder(BorderFactory.createLineBorder(new Color(200, 200, 150), 2));
        
        // 위로 가기 아이콘 생성
        JLabel iconLabel = new JLabel("⬆");
        iconLabel.setFont(new Font("Dialog", Font.BOLD, 48));
        iconLabel.setHorizontalAlignment(JLabel.CENTER);
        iconLabel.setForeground(new Color(100, 100, 100));
        
        // 위로 가기 텍스트
        JLabel nameLabel = new JLabel("<html><center><b>위로 가기</b></center></html>");
        nameLabel.setHorizontalAlignment(JLabel.CENTER);
        nameLabel.setFont(new Font("Dialog", Font.BOLD, 11));
        
        upPanel.add(iconLabel, BorderLayout.CENTER);
        upPanel.add(nameLabel, BorderLayout.SOUTH);
        
        // 마우스 이벤트
        upPanel.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 1 || e.getClickCount() == 2) {
                    navigateToDirectory(parentDir);
                }
            }
            
            @Override
            public void mouseEntered(MouseEvent e) {
                upPanel.setBackground(new Color(255, 255, 180));
                upPanel.setCursor(new Cursor(Cursor.HAND_CURSOR));
            }
            
            @Override
            public void mouseExited(MouseEvent e) {
                upPanel.setBackground(new Color(255, 255, 220));
                upPanel.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
            }
        });
        
        return upPanel;
    }
    
    // 파일 아이콘 패널 생성
    private JPanel createFileIconPanel(File file) {
        JPanel fileIconPanel = new JPanel();
        fileIconPanel.setLayout(new BorderLayout(5, 5));
        fileIconPanel.setPreferredSize(new Dimension(100, 120));
        fileIconPanel.setBackground(Color.WHITE);
        fileIconPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
        
        // 시스템 아이콘 가져오기
        Icon systemIcon = fileSystemView.getSystemIcon(file);
        
        // 아이콘을 더 크게 스케일링
        ImageIcon scaledIcon = null;
        if (systemIcon instanceof ImageIcon) {
            ImageIcon imageIcon = (ImageIcon) systemIcon;
            Image image = imageIcon.getImage();
            Image scaledImage = image.getScaledInstance(48, 48, Image.SCALE_SMOOTH);
            scaledIcon = new ImageIcon(scaledImage);
        } else {
            // ImageIcon이 아닌 경우 기본 크기로 사용
            scaledIcon = new ImageIcon();
            // 기본 아이콘 설정
            if (systemIcon != null) {
                scaledIcon = new ImageIcon(new java.awt.image.BufferedImage(48, 48, java.awt.image.BufferedImage.TYPE_INT_ARGB));
                Graphics g = ((ImageIcon)scaledIcon).getImage().getGraphics();
                systemIcon.paintIcon(null, g, 0, 0);
                g.dispose();
            }
        }
        
        JLabel iconLabel = new JLabel(scaledIcon);
        iconLabel.setHorizontalAlignment(JLabel.CENTER);
        
        // 파일명 레이블
        String fileName = file.getName();
        if (fileName.length() > 15) {
            fileName = fileName.substring(0, 12) + "...";
        }
        JLabel nameLabel = new JLabel("<html><center>" + fileName + "</center></html>");
        nameLabel.setHorizontalAlignment(JLabel.CENTER);
        nameLabel.setFont(new Font("Dialog", Font.PLAIN, 10));
        
        fileIconPanel.add(iconLabel, BorderLayout.CENTER);
        fileIconPanel.add(nameLabel, BorderLayout.SOUTH);
        
        // 마우스 클릭 이벤트
        fileIconPanel.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    if (file.isDirectory()) {
                        navigateToDirectory(file);
                    } else if (isTextFile(file)) {
                        openTextViewer(file);
                    } else {
                        // 다른 파일 타입은 시스템 기본 프로그램으로 열기 시도
                        try {
                            if (Desktop.isDesktopSupported()) {
                                Desktop.getDesktop().open(file);
                            }
                        } catch (Exception ex) {
                            JOptionPane.showMessageDialog(
                                FileExplorer.this,
                                "파일을 열 수 없습니다: " + ex.getMessage(),
                                "오류",
                                JOptionPane.ERROR_MESSAGE
                            );
                        }
                    }
                }
            }
            
            @Override
            public void mouseEntered(MouseEvent e) {
                fileIconPanel.setBackground(new Color(230, 240, 255));
                fileIconPanel.setCursor(new Cursor(Cursor.HAND_CURSOR));
            }
            
            @Override
            public void mouseExited(MouseEvent e) {
                fileIconPanel.setBackground(Color.WHITE);
                fileIconPanel.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
            }
        });
        
        return fileIconPanel;
    }
    
    // 디렉토리로 네비게이션
    private void navigateToDirectory(File directory) {
        if (directory == null || !directory.isDirectory()) {
            return;
        }
        
        currentDirectory = directory;
        pathField.setText(directory.getAbsolutePath());
        
        // 트리에서 해당 경로까지 확장하고 선택
        expandAndSelectTreePath(directory);
        
        // 파일 목록 업데이트 (테이블과 아이콘 뷰 모두)
        updateTable(directory);
    }
    
    // 트리에서 디렉토리 경로를 확장하고 선택
    private void expandAndSelectTreePath(File targetDirectory) {
        DefaultMutableTreeNode root = (DefaultMutableTreeNode) tree.getModel().getRoot();
        
        // 경로를 상위부터 하위로 분해
        java.util.List<File> pathList = new java.util.ArrayList<>();
        File current = targetDirectory;
        while (current != null) {
            pathList.add(0, current);
            current = current.getParentFile();
        }
        
        // 루트에서 시작하여 경로를 따라 노드를 찾고 확장
        DefaultMutableTreeNode currentNode = root;
        
        for (File pathFile : pathList) {
            DefaultMutableTreeNode foundNode = null;
            
            // 현재 노드의 자식 중에서 pathFile과 일치하는 노드 찾기
            for (int i = 0; i < currentNode.getChildCount(); i++) {
                DefaultMutableTreeNode childNode = (DefaultMutableTreeNode) currentNode.getChildAt(i);
                Object userObject = childNode.getUserObject();
                
                if (userObject instanceof File) {
                    File childFile = (File) userObject;
                    if (childFile.getAbsolutePath().equals(pathFile.getAbsolutePath())) {
                        foundNode = childNode;
                        break;
                    }
                }
            }
            
            if (foundNode != null) {
                // 노드를 찾았으면 확장
                TreePath path = new TreePath(((DefaultTreeModel) tree.getModel()).getPathToRoot(foundNode));
                tree.expandPath(path);
                
                // 하위 디렉토리 로드
                loadChildren(foundNode);
                
                currentNode = foundNode;
            } else {
                // 노드를 찾지 못하면 중단
                break;
            }
        }
        
        // 최종 노드 선택
        if (currentNode != root) {
            TreePath finalPath = new TreePath(((DefaultTreeModel) tree.getModel()).getPathToRoot(currentNode));
            tree.setSelectionPath(finalPath);
            tree.scrollPathToVisible(finalPath);
        }
    }
    
    // 텍스트 파일인지 확인 (중복 제거를 위해 주석 처리)
    /*
    private boolean isTextFile(File file) {
        String name = file.getName().toLowerCase();
        String[] textExtensions = {".txt", ".log", ".java", ".xml", ".html", 
                                   ".css", ".js", ".json", ".md", ".csv", 
                                   ".properties", ".ini", ".cfg", ".conf"};
        
        for (String ext : textExtensions) {
            if (name.endsWith(ext)) {
                return true;
            }
        }
        return false;
    }
    */
    
    // 텍스트 뷰어 열기
    private void openTextViewer(File file) {
        new TextViewerWindow(file);
    }
    
    // 텍스트 뷰어 창 클래스
    class TextViewerWindow extends JFrame {
        private JTextArea textArea;
        private File currentFile;
        
        public TextViewerWindow(File file) {
            this.currentFile = file;
            
            setTitle(file.getName() + " - 텍스트 뷰어");
            setSize(700, 500);
            setLocationRelativeTo(FileExplorer.this);
            
            // 텍스트 영역 생성
            textArea = new JTextArea();
            textArea.setEditable(false);
            textArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
            textArea.setLineWrap(true);
            textArea.setWrapStyleWord(true);
            
            JScrollPane scrollPane = new JScrollPane(textArea);
            add(scrollPane, BorderLayout.CENTER);
            
            // 하단 패널 - 파일 정보
            JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
            long fileSize = file.length();
            String sizeInfo = "크기: " + formatFileSize(fileSize);
            JLabel infoLabel = new JLabel(sizeInfo);
            bottomPanel.add(infoLabel);
            add(bottomPanel, BorderLayout.SOUTH);
            
            // 파일 내용 읽기
            loadFileContent();
            
            setVisible(true);
        }
        
        private void loadFileContent() {
            try {
                // 파일이 너무 큰 경우 경고
                if (currentFile.length() > 5 * 1024 * 1024) { // 5MB 이상
                    int result = JOptionPane.showConfirmDialog(
                        this,
                        "파일이 " + formatFileSize(currentFile.length()) + 
                        "로 큽니다. 열기를 계속하시겠습니까?",
                        "큰 파일 경고",
                        JOptionPane.YES_NO_OPTION,
                        JOptionPane.WARNING_MESSAGE
                    );
                    
                    if (result != JOptionPane.YES_OPTION) {
                        dispose();
                        return;
                    }
                }
                
                // 파일 읽기
                java.io.BufferedReader reader = new java.io.BufferedReader(
                    new java.io.FileReader(currentFile)
                );
                
                StringBuilder content = new StringBuilder();
                String line;
                int lineCount = 0;
                
                while ((line = reader.readLine()) != null) {
                    content.append(line).append("\n");
                    lineCount++;
                }
                
                reader.close();
                
                textArea.setText(content.toString());
                textArea.setCaretPosition(0); // 처음으로 스크롤
                
                setTitle(currentFile.getName() + " - 텍스트 뷰어 (" + lineCount + " 줄)");
                
            } catch (java.io.IOException e) {
                JOptionPane.showMessageDialog(
                    this,
                    "파일을 읽을 수 없습니다: " + e.getMessage(),
                    "오류",
                    JOptionPane.ERROR_MESSAGE
                );
                dispose();
            }
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception e) {
                e.printStackTrace();
            }
            
            FileExplorer explorer = new FileExplorer();
            explorer.setVisible(true);
        });
    }
}

/**
 * FlowLayout의 서브클래스로, 컴포넌트가 줄바꿈되도록 함
 */
class WrapLayout extends FlowLayout {
    public WrapLayout() {
        super();
    }
    
    public WrapLayout(int align) {
        super(align);
    }
    
    public WrapLayout(int align, int hgap, int vgap) {
        super(align, hgap, vgap);
    }
    
    @Override
    public Dimension preferredLayoutSize(Container target) {
        return layoutSize(target, true);
    }
    
    @Override
    public Dimension minimumLayoutSize(Container target) {
        Dimension minimum = layoutSize(target, false);
        minimum.width -= (getHgap() + 1);
        return minimum;
    }
    
    private Dimension layoutSize(Container target, boolean preferred) {
        synchronized (target.getTreeLock()) {
            int targetWidth = target.getSize().width;
            Container container = target;
            
            while (container.getSize().width == 0 && container.getParent() != null) {
                container = container.getParent();
            }
            
            targetWidth = container.getSize().width;
            
            if (targetWidth == 0) {
                targetWidth = Integer.MAX_VALUE;
            }
            
            int hgap = getHgap();
            int vgap = getVgap();
            java.awt.Insets insets = target.getInsets();
            int horizontalInsetsAndGap = insets.left + insets.right + (hgap * 2);
            int maxWidth = targetWidth - horizontalInsetsAndGap;
            
            Dimension dim = new Dimension(0, 0);
            int rowWidth = 0;
            int rowHeight = 0;
            
            int nmembers = target.getComponentCount();
            
            for (int i = 0; i < nmembers; i++) {
                Component m = target.getComponent(i);
                
                if (m.isVisible()) {
                    Dimension d = preferred ? m.getPreferredSize() : m.getMinimumSize();
                    
                    if (rowWidth + d.width > maxWidth) {
                        addRow(dim, rowWidth, rowHeight);
                        rowWidth = 0;
                        rowHeight = 0;
                    }
                    
                    if (rowWidth != 0) {
                        rowWidth += hgap;
                    }
                    
                    rowWidth += d.width;
                    rowHeight = Math.max(rowHeight, d.height);
                }
            }
            
            addRow(dim, rowWidth, rowHeight);
            
            dim.width += horizontalInsetsAndGap;
            dim.height += insets.top + insets.bottom + vgap * 2;
            
            Container scrollPane = javax.swing.SwingUtilities.getAncestorOfClass(JScrollPane.class, target);
            
            if (scrollPane != null && target.isValid()) {
                dim.width -= (hgap + 1);
            }
            
            return dim;
        }
    }
    
    private void addRow(Dimension dim, int rowWidth, int rowHeight) {
        dim.width = Math.max(dim.width, rowWidth);
        
        if (dim.height > 0) {
            dim.height += getVgap();
        }
        
        dim.height += rowHeight;
    }
}

```

