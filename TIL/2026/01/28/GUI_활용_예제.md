# GUI 활용 예제

> 날짜: 2026-01-28
> 원본 노션: [링크](https://www.notion.so/GUI-2f7b28703eb080b2bcc9f6e2ed66ae46)

---

```java
package gui;

import javax.swing.*;
import java.awt.*;

public class Calculator extends JFrame {
	public Calculator() {
		setTitle("자바 계산기");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLayout(new BorderLayout());

		// 1. 상단 결과창
		JTextField display = new JTextField("0");
		display.setEditable(false);
		display.setHorizontalAlignment(JTextField.RIGHT);
		display.setFont(new Font("Arial", Font.BOLD, 25));
		add(display, BorderLayout.NORTH);

		// 2. 중앙 버튼 패널
		JPanel buttonPanel = new JPanel();
		buttonPanel.setLayout(new GridLayout(4, 4, 5, 5));

		String[] buttons = { "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", "C", "=", "+" };

		for (String text : buttons) {
			JButton btn = new JButton(text);
			btn.setFont(new Font("Arial", Font.PLAIN, 18));
			buttonPanel.add(btn);
		}

		add(buttonPanel, BorderLayout.CENTER);

		setSize(300, 400);
		setVisible(true);
	}

	public static void main(String[] args) {
		new Calculator();
	}
}

```

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

```java
package gui;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.*;
import javax.swing.*;

/* 자바 그래픽
 * AWT	  : OS에 맞춰서 움직인다. OS화면 이미지를 가져온다. -> 느림 
 * Swing  : JVM에서 이미지를 가져오기 look and feel -> 자바가 가져옴 -> 빠름 
 * javaFX : 보다 효율적으로 그래픽을 사용하기 위해서 나옴 -> css / xml
 */


public class Final {

	   public static void main(String[] args) {
	      JFrame jf = new JFrame();
	      jf.setSize(800, 600); //사이즈
	      jf.setTitle("최종 정리"); //타이틀
	      
	      //layout
	      GridLayout gl = new GridLayout(3, 2, 10,10);
	      jf.setLayout(gl);
	      
	      //jlabel : 글자만 사용할 수 있는 객체
	      final JLabel jl = new JLabel("이름");
	      jl.setText("이름은?");
	      jf.add(jl);
	      
	      //button
	      final JButton jb = new JButton();
	      jb.setText("버튼");
	      jf.add(jb);
	      
	      JFileChooser jfc = new JFileChooser();
	      jf.add(jfc);
	      
	      final JTextField jtf = new JTextField();
	      jf.add(jtf);
	      
	      //이벤트처리 : 이벤트가 일어나는 객체에 Listener를 지정해서 사용합니다.
	      jb.addActionListener(new ActionListener() {
	         
	         @Override
	         public void actionPerformed(ActionEvent e) {
	            jl.setText("버튼 누름");//만약 버튼이 눌렸으면 Jlabel에 이 글씨가 써짐
	            jl.setForeground(Color.GRAY);//배경색 바꾸기
	            jl.setBackground(Color.black);
	            jb.setForeground(Color.CYAN);//버튼의 배경색 바꾸기
	         }
	      });
	      
	      JPanel jp = new JPanel();
	      jp.setLayout(new GridLayout(1, 2));
	      
	      JButton jbtn = new JButton();
	      jbtn.setText("버튼 두 개짜리");
	      jp.add(jbtn);//버튼1
	      
	      jp.add(new JButton());//버튼2
	      
	      jf.add(jp);
	      
	      jf.setVisible(true);
	      
	      jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	   }

	}

```

```java
package gui;

import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Image;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.SwingConstants;

public class LoginView extends JFrame {
	public LoginView() {
		setTitle("로그인 시스템");
		setSize(300, 150);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLocationRelativeTo(null); // 화면 중앙에 배치

		// 메인 패널 (2행 2열 레이아웃)
		JPanel panel = new JPanel(new GridLayout(3, 2, 5, 5));

		panel.add(new JLabel(" 아이디:"));
		JTextField idField = new JTextField();
		panel.add(idField);

		panel.add(new JLabel(" 비밀번호:"));
		JPasswordField pwField = new JPasswordField();
		panel.add(pwField);

		JButton loginBtn = new JButton("로그인");
		JButton cancelBtn = new JButton("취소");
		panel.add(loginBtn);
		panel.add(cancelBtn);

		add(panel);
		setVisible(true);

		// 이벤트 처리
		loginBtn.addActionListener(e -> {
			String id = idField.getText();
			String pw = new String(pwField.getPassword());
			if (id.equals("admin") && pw.equals("1234")) {
				JOptionPane.showMessageDialog(this, "로그인 성공!");
				this.dispose(); //페이지 전환을 위해 기존 페이지 닫기
				// setVisible(false)는 화면만 안 보여줌 = 자원 사용 중
				new MainView(id); // 새로운 페이지 열기 
			} else {
				JOptionPane.showMessageDialog(this, "로그인 실패..");
			}
		});
	}

	public static void main(String[] args) {
		new LoginView();
	}
}

class MainView extends JFrame {
    public MainView(String userId) {
        setTitle("로그인후 보여지는 화면");
        setSize(500, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        
        ImageIcon oriImg = new ImageIcon("src/images/lock.png");
        Image img = oriImg.getImage();
     // 화면 크기에 맞게 이미지 축소/확대
        Image scaledImg = img.getScaledInstance(300, 300, Image.SCALE_SMOOTH);
        ImageIcon scaledIcon = new ImageIcon(scaledImg);

        // 2. 이미지를 담은 라벨 생성
        JLabel imageLabel = new JLabel(scaledIcon);
        JLabel textLabel = new JLabel(userId + "님, 환영합니다!", SwingConstants.CENTER);
        textLabel.setFont(new Font("맑은 고딕", Font.BOLD, 20));

        panel.add(imageLabel, BorderLayout.CENTER);
        panel.add(textLabel, BorderLayout.SOUTH);
        
        
        add(panel);
        setVisible(true); // 창 표시
    }
}
```

```java
package gui;

import java.awt.event.InputEvent;

import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.KeyStroke;

public class Menu {
   JFrame jf = new JFrame("메뉴 만들기");
   
   JTextArea textArea = new JTextArea("입력하세요.", 5,10);//스크롤바가 없는 5X10박스형태
   
   //스크롤바 만들기
   JScrollPane jScrollPane = new JScrollPane(textArea);
   
   //메뉴 넣기
   JMenuBar menuBar = new JMenuBar();
   JMenu fileMenu = new JMenu("파일");
   JMenu helpMenu = new JMenu("도움말");
   
   public Menu() {
      fileMenu.add(new JMenuItem("새파일 열기"));
      fileMenu.getItem(0).setAccelerator(
            KeyStroke.getKeyStroke('N',InputEvent.CTRL_MASK ^ InputEvent.ALT_MASK)
            );
      fileMenu.add(new JMenuItem("저장"));
      fileMenu.add(new JMenuItem("기존파일에 추가"));
      fileMenu.addSeparator();//구분선? --------------
      fileMenu.add(new JMenuItem("종료"));
      
      helpMenu.add(new JMenuItem("이 프로그램은"));
      helpMenu.add(new JMenuItem("만든 사람"));
      
      menuBar.add(fileMenu);
      menuBar.add(helpMenu);//메뉴바에 보여지도록 붙이기
      
      jf.setJMenuBar(menuBar);//프레임에 메뉴가 보여지도록 붙이기
      
      jf.add(jScrollPane, "Center");//스크롤이 들어간 글쓰기 영역을 붙이기
      
      jf.setSize(300, 600);
      
      jf.setVisible(true);
      
      jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
   }
   
   public static void main(String[] args) {
      new Menu();
   }   

}
```

```java
package gui;

/**
 * Notepad입니다.
 * <p>wisejia.com</p>
 * seoul, Korea
 * 2024-07-10 첫판을 만듬
 * 2024-07-11 서체 선택을 넣음 
 * 
 * 참고한 코드 
 * 서체 선택 FontChooser = 
 * https://bhiggs.x10hosting.com/Courses/JavaProgramming/Swing/Dialogs/FontChooserDialog.htm
 * @author      poseidon
 * @since       1.0
 **/
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.print.PrinterException;
import java.io.*;
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.filechooser.FileNameExtensionFilter;

public class Notepad extends JFrame {
	private static final long serialVersionUID = 1L;
	Toolkit toolkit = Toolkit.getDefaultToolkit();
	JTextArea jTextArea = new JTextArea();
	String path = "";// 경로 자장하기
	static int countLine = 0;// 현 화면에 호출된 줄 수
	Font defaultFont = new Font("맑은 고딕", Font.PLAIN, 20);
	final static String cancel = "작업을 취소했습니다.";
	JFileChooser fileChooser = new JFileChooser(System.getProperty("user.home") + "\\Desktop\\");
	Border empty = BorderFactory.createEmptyBorder(5, 5, 5, 5);// 여백주기
	JScrollPane jScrollPane = new JScrollPane(jTextArea);
	JPanel bottom = new JPanel();
	JLabel bottomField = new JLabel("Notepad를 시작합니다.");
	JLabel bottomInfo = new JLabel("줄 1, 열 0, 글자수 0");
	JLabel bottomFontInfo = new JLabel(defaultFont.getFontName() + " / " + defaultFont.getSize());

	JMenuBar jMenuBar = new JMenuBar();
	JMenu menuFile = new JMenu("파일");
	JMenu menuEdit = new JMenu("편집");
	JMenu menuView = new JMenu("보기");
	JMenu menuHelp = new JMenu("도움말");

	// JMenuItem newTeb = new JMenuItem("새 탭");
	JMenuItem newWindow = new JMenuItem("새 창");
	JMenuItem open = new JMenuItem("열기");
	JMenuItem save = new JMenuItem("저장");
	JMenuItem print = new JMenuItem("인쇄");
	JMenuItem closeWindow = new JMenuItem("닫기");
	JMenuItem selectAll = new JMenuItem("모두 선택");
	JMenuItem help = new JMenuItem("도움말");
	JMenuItem login = new JMenuItem("로그인");

	public Notepad() {
		super("제목없음"); // 부모 생성자
		setIconImage(toolkit.getImage("c:\\temp\\trident.png")); // 아이콘 변경하기
		setMenu();// 메뉴 조립하기

		this.add(jMenuBar, BorderLayout.NORTH);

		jTextArea.setBorder(empty);
		jTextArea.setFont(defaultFont); // 서체 크기
		// keyTyped(KeyEvent e) 키가 때어졌을 때 (=keyReleased)
		jTextArea.addKeyListener(eventJTextAreaKeyTyped());// 글자 수 라인수 얻는 이벤트 만들기
		jScrollPane = new JScrollPane(jTextArea);
		this.add(jScrollPane, BorderLayout.CENTER);

		this.add(bottom, BorderLayout.SOUTH);
		bottom.setBorder(empty);
		bottom.setLayout(new GridLayout(1, 3));// 화면 하단을 5개로 나눔
		bottom.add(bottomInfo);
		bottom.add(bottomFontInfo);
		bottomField.setHorizontalAlignment(JLabel.RIGHT);
		bottom.add(bottomField);
		this.add(bottom, BorderLayout.SOUTH);

		this.setLocationRelativeTo(null);//화면 중앙에
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setSize(1000, 600);
		this.setVisible(true);
	}

	private KeyListener eventJTextAreaKeyTyped() {// jTextArea에 입력된 글자수, 라인수 검사
		KeyListener kl = new KeyListener() {
			@Override
			public void keyTyped(KeyEvent e) {
				bottomInfo.setText("줄 " + jTextArea.getLineCount() + 
						", 열 " + jTextArea.getRows() + 
						", 글자수 "	+ jTextArea.getText().length());// 왜 열 수를 안 가져오지
			}
			@Override
			public void keyReleased(KeyEvent e) {}

			@Override
			public void keyPressed(KeyEvent e) {}
		};
		return kl;
	}

	void setMenu() {
		jMenuBar.setBorder(empty);
		newWindow.setAccelerator(KeyStroke.getKeyStroke('N', InputEvent.CTRL_DOWN_MASK));
		newWindow.addActionListener(eventNewWindow());
		menuFile.add(newWindow);

		open.setAccelerator(KeyStroke.getKeyStroke('O', InputEvent.CTRL_DOWN_MASK));
		open.addActionListener(eventOpenFile());
		menuFile.add(open);

		save.setAccelerator(KeyStroke.getKeyStroke('S', InputEvent.CTRL_DOWN_MASK));
		save.addActionListener(eventSave());
		menuFile.add(save);
		menuFile.addSeparator(); // 구분선 -----------------------

		print.setAccelerator(KeyStroke.getKeyStroke('P', InputEvent.CTRL_DOWN_MASK));
		print.addActionListener(eventPrint());
		menuFile.add(print);
		closeWindow.setAccelerator(KeyStroke.getKeyStroke('X', InputEvent.CTRL_DOWN_MASK));
		closeWindow.addActionListener(eventExit());
		menuFile.add(closeWindow);

		JMenuItem font = new JMenuItem("서체");
		font.addActionListener(eventFont());
		menuEdit.add(font);

		menuEdit.add(new JMenuItem("실행취소"));
		menuEdit.add(new JMenuItem("복사"));
		menuEdit.add(new JMenuItem("잘라내기"));
		menuEdit.add(new JMenuItem("붙여넣기"));
		menuEdit.addSeparator();// 구분선 넣기
		selectAll.setAccelerator(KeyStroke.getKeyStroke('A', InputEvent.CTRL_DOWN_MASK));
		menuEdit.add(selectAll);
		selectAll.addActionListener(eventSelectAll());

		menuView.add(new JMenuItem("확대축소"));
		menuView.add(new JMenuItem("상태 표시줄"));
		menuView.add(new JMenuItem("자동 줄바꿈"));

		login.addActionListener(eventLogin());
		menuHelp.add(login);
		help.addActionListener(eventHelp());
		menuHelp.add(help);

		jMenuBar.add(menuFile);
		jMenuBar.add(menuEdit);
		jMenuBar.add(menuView);
		jMenuBar.add(menuHelp);
	}

	private ActionListener eventLogin() {
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				JDialog login = new JDialog();
				//JTextField id = new JTextField();
				JPasswordField pw = new JPasswordField(10);
				JButton loginBtn = new JButton("LOGON");
				login.setTitle("Logon");
				login.setLayout(new FlowLayout());
				login.add(pw);
				login.add(loginBtn);
				login.setSize(300, 300);
				login.setVisible(true);
			}
		};
		return ac;
	}

	private ActionListener eventPrint() {
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					jTextArea.print(null, null, true, null, null, false);
				} catch (PrinterException e1) {
					e1.printStackTrace();
				}
			}
		};
		return ac;
	}

	private ActionListener eventFont() {// font변경
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// 다른 사람이 개발한 폰트 선택 창입니다. https://bhiggs.x10hosting.com/Courses/JavaProgramming/Swing/Dialogs/FontChooserDialog.htm
//				Font font = FontChooser.showDialog(jTextArea, "서체를 선택하세요");
//				if (font != null) {// 서체 변경을 하지 않은 경우 방지용
//					jTextArea.setFont(font);// 조금 더 좋은 방법이 없을까?
//					defaultFont = font;
//					bottomField.setText("서체가 " + defaultFont.getFontName() + "으로 변경되었습니다.");
//					bottomFontInfo.setText(defaultFont.getFontName() + " / " + defaultFont.getSize());
//				}
			}
		};
		return ac;
	}

	private String readFile(File file) {
		StringBuilder sb = new StringBuilder();
		try {
			BufferedReader br = new BufferedReader(new FileReader(file));
			String read = "";
			bottomField.setText("파일을 읽고 있습니다.");
			while ((read = br.readLine()) != null) {
				sb.append(read + System.lineSeparator());
				countLine++;
			}
			br.close();
			bottomField.setText(file.getName() + " 파일을 불러왔습니다.");
			this.setTitle(file.getName());
			path = file.getPath(); // 경로 저장하기
		} catch (FileNotFoundException e) {
			bottomField.setText("파일이 없습니다. 다시 확인해주세요.");
		} catch (IOException e) {
			bottomField.setText("파일을 읽을 수 없습니다");
		}
		return sb.toString();
	}

	private void saveFile(File file) {
		try {
			PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(file)));
			pw.write(jTextArea.getText());
			pw.flush();
			pw.close();
		} catch (IOException e) {
			bottomField.setText("파일을 저장하지 못했습니다.");
		}
		bottomField.setText("파일을 저장했습니다.");
		setTitle(file.getName());
	}

	public static void main(String[] args) {
		new Notepad();
	}

	private ActionListener eventNewWindow() {
		ActionListener al = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				setTitle("제목없음");
				path = ""; // 경로 초기화
				jTextArea.setText("");
				bottomField.setText("새로운 창으로 변경합니다.");
			}
		};
		return al;
	}

	private ActionListener eventOpenFile() {
		ActionListener al = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// 파일선택 : 윈도우의 경우 사용자 폴더의 desktop으로 연결하기
				fileChooser.setFileFilter(new FileNameExtensionFilter("TEXT FILES", "txt", "text")); // 파일 txt만
				fileChooser.showOpenDialog(jTextArea);
				File openFile = fileChooser.getSelectedFile();
				if (openFile != null) {
					String text = readFile(fileChooser.getSelectedFile());
					jTextArea.setText(text);
				} else {
					bottomField.setText(cancel);
				}
			}
		};
		return al;
	}

	private ActionListener eventExit() {
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				dispose();// 프레임 닫기 : 여러 프레임이 떠 있을 경우 하나의 프레임만 닫기
			}
		};
		return ac;
	}

	private ActionListener eventHelp() {
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(jTextArea,
						"Notepad 프로그램 1.0.0\n제작날짜 : 2024년 7월 10일\n" 
							+ "제작자 : poseidon\nemail : poseidon@kakao.com\n"
							+ "blog : blog.naver.com/wisejia\n기 타 : 서체 선택 기능은 다른 사람의 작품임",
						"정보", JOptionPane.INFORMATION_MESSAGE, new ImageIcon("c:\\temp\\trident.png"));
			}
		};
		return ac;
	}

	private ActionListener eventSelectAll() {
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				jTextArea.selectAll();
				bottomField.setText("전체 선택");
			};
		};
		return ac;
	}

	private ActionListener eventSave() {
		ActionListener ac = new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if (path == "") {// 새로 저장하기
					fileChooser.setFileFilter(new FileNameExtensionFilter("TEXT FILES", "txt", "text")); // 파일 txt만
					if (fileChooser.showSaveDialog(Notepad.this) != fileChooser.CANCEL_OPTION) {
						File newFile = fileChooser.getSelectedFile();// 저장 위치 선택하기
						String newFileName = newFile.toString();
						if (!(newFileName.substring(newFileName.length() - 4, newFileName.length() - 3).equals("."))) {
							newFile = new File(newFileName + ".txt");// 파일명이 없으면 .txt붙여주기
						}
						bottomField.setText("새로운 파일을 저장합니다.");
						saveFile(newFile);// 파일저장하기
					} else { // 파일이 선택 안 됨.
						bottomField.setText(cancel);
					}

				} else { // 기존 파일에 저장하기
					saveFile(new File(path));
				}
			};
		};
		return ac;
	}

	// 추가할 기능
	// keyPressed(KeyEvent e) 키가 눌렸을 때
	// keyReleased(KeyEvent e) 키가 때어졌을 때
	// keyTyped(KeyEvent e) 키가 때어졌을 때 (=keyReleased)
}
```

