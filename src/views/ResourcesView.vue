<template>
  <div class="page-view" @dragover.prevent="pageDragover = true" @dragleave="pageDragover = false" @drop.prevent="handlePageDrop">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-left">
          <h1>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" class="header-icon"><path d="M2 6C2 4.9 2.9 4 4 4h5l2 3h9c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6Z" fill="#f5a623"/></svg>
            资源中心
          </h1>
          <p class="page-subtitle">社团内部资源共享平台</p>
        </div>
        <div class="header-stats" v-if="stats">
          <div class="stat-item">
            <span class="stat-value">{{ stats.totalFiles }}</span>
            <span class="stat-label">文件</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">{{ formatSize(stats.totalSize) }}</span>
            <span class="stat-label">已用</span>
          </div>
        </div>
      </div>

      <!-- 工具栏 -->
      <div class="toolbar-card">
        <div class="toolbar-main">
          <div class="search-wrap">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <input v-model="search" @input="debouncedLoad" placeholder="搜索文件名称或描述..." class="search-input" />
            <button v-if="search" class="search-clear" @click="search=''; debouncedLoad()">&times;</button>
          </div>
          <div class="filter-group">
            <select v-model="filterCategory" @change="loadResources" class="filter-select">
              <option value="">全部分类</option>
              <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
            </select>
            <select v-if="tags.length" v-model="filterTag" @change="loadResources" class="filter-select">
              <option value="">全部标签</option>
              <option v-for="t in tags" :key="t.name" :value="t.name">{{ t.name }} ({{ t.count }})</option>
            </select>
          </div>
          <div class="action-group">
            <button class="btn btn-outline" @click="showCreateFolder = true">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
              新建文件夹
            </button>
            <button class="btn btn-primary" @click="showUpload = true">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
              上传资源
            </button>
          </div>
        </div>
      </div>

      <!-- 批量操作栏 -->
      <transition name="fade">
        <div v-if="selectedIds.size > 0" class="batch-bar">
          <div class="batch-left">
            <div class="batch-badge">{{ selectedIds.size }}</div>
            <span class="batch-text">项已选择</span>
          </div>
          <div class="batch-actions">
            <button class="btn btn-outline" @click="handleBatchDownload">批量下载</button>
            <button class="btn btn-text" @click="selectedIds.clear()">取消选择</button>
          </div>
        </div>
      </transition>

      <!-- 面包屑 -->
      <div class="breadcrumb-bar">
        <button class="breadcrumb-link" :class="{ active: !currentFolder }" @click="navigateTo(null)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
          全部文件
        </button>
        <template v-for="item in breadcrumb" :key="item.id">
          <svg class="breadcrumb-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
          <button class="breadcrumb-link active" @click="navigateTo(item.id)">{{ item.name }}</button>
        </template>
      </div>

      <!-- 全局拖拽提示 -->
      <transition name="fade">
        <div v-if="pageDragover" class="global-drop-overlay">
          <div class="global-drop-content">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--warm-terracotta)" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
            <span>释放文件以上传至当前文件夹</span>
          </div>
        </div>
      </transition>

      <!-- 加载中 -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>

      <template v-else>
        <!-- 表头 -->
        <div class="list-header">
          <div class="lh-check"><input type="checkbox" :checked="isAllChecked" @change="toggleSelectAll" /></div>
          <div class="lh-name sortable" @click="toggleSort('name')">名称 <span class="sort-arrow" :class="{ down: sortKey === 'name' && sortDir === 'desc', active: sortKey === 'name' }">▾</span></div>
          <div class="lh-size sortable" @click="toggleSort('size')">大小 <span class="sort-arrow" :class="{ down: sortKey === 'size' && sortDir === 'desc', active: sortKey === 'size' }">▾</span></div>
          <div class="lh-uploader">上传者</div>
          <div class="lh-date sortable" @click="toggleSort('date')">时间 <span class="sort-arrow" :class="{ down: sortKey === 'date' && sortDir === 'desc', active: sortKey === 'date' }">▾</span></div>
          <div class="lh-actions">操作</div>
        </div>

        <div class="list-body">
          <!-- 文件夹 -->
          <div v-for="folder in sortedFolders" :key="'f-'+folder.id" class="list-row folder" @dblclick="renamingId===folder.id?null:navigateTo(folder.id)">
            <div class="lr-check" @click.stop><input type="checkbox" :checked="selectedIds.has('f-'+folder.id)" @change="toggleSelect('f-'+folder.id)" /></div>
            <div class="lr-name">
              <span class="lr-icon" v-html="iconSvg('folder')"></span>
              <template v-if="renamingId===folder.id">
                <input v-model="renamingName" class="rename-input" @keyup.enter="confirmRename()" @keyup.escape="renamingId=null" @click.stop />
              </template>
              <span v-else class="lr-text">{{ folder.name }}</span>
            </div>
            <div class="lr-size">—</div>
            <div class="lr-uploader">{{ folder.uploader_name || '-' }}</div>
            <div class="lr-date">{{ formatDate(folder.updated_at || folder.created_at) }}</div>
            <div class="lr-actions" @click.stop>
              <template v-if="renamingId===folder.id">
                <button class="icon-btn green" title="确认" @click="confirmRename()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg></button>
                <button class="icon-btn" title="取消" @click="renamingId=null"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
              </template>
              <template v-else>
                <button class="icon-btn" title="重命名" @click="startRename(folder)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg></button>
                <button class="icon-btn" title="分享" @click="handleShare(folder)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 3.9M15.4 6.6l-6.8 3.9"/></svg></button>
              </template>
            </div>
          </div>

          <!-- 文件 -->
          <div v-for="file in sortedFiles" :key="'r-'+file.id" class="list-row">
            <div class="lr-check"><input type="checkbox" :checked="selectedIds.has('r-'+file.id)" @change="toggleSelect('r-'+file.id)" /></div>
            <div class="lr-name">
              <img v-if="isImageExt(file.file_ext) && file.file_url" :src="file.file_url" class="lr-thumb" @error="$event.target.remove()" />
              <span v-else class="lr-icon" v-html="iconSvg(file.file_ext)"></span>
              <div class="lr-name-inner">
                <template v-if="renamingId === file.id">
                  <input v-model="renamingName" class="rename-input" @keyup.enter="confirmRename()" @keyup.escape="renamingId=null" />
                </template>
                <div v-else class="lr-name-wrap">
                  <span class="lr-text">{{ file.original_name || file.name }}</span>
                  <div class="hover-card">
                    <div class="hover-title">{{ file.original_name || file.name }}</div>
                    <div v-if="file.category" class="hover-tag">{{ file.category }}</div>
                    <div v-if="file.description" class="hover-desc">{{ file.description }}</div>
                    <div class="hover-grid">
                      <span>大小 {{ formatSize(file.file_size) }}</span>
                      <span>类型 {{ (file.file_ext||'').toUpperCase() }}</span>
                      <span>上传 {{ file.uploader_name || '-' }}</span>
                      <span>下载 {{ file.download_count }} 次</span>
                    </div>
                    <div v-if="file.tags?.length" class="hover-tags">
                      <span v-for="t in file.tags" :key="t" class="tag-sm">{{ t }}</span>
                    </div>
                  </div>
                </div>
                <span v-if="file.category" class="lr-tag">{{ file.category }}</span>
              </div>
            </div>
            <div class="lr-size">{{ formatSize(file.file_size) }}</div>
            <div class="lr-uploader">{{ file.uploader_name || '-' }}</div>
            <div class="lr-date">{{ formatDate(file.updated_at || file.created_at) }}</div>
            <div class="lr-actions">
              <template v-if="renamingId===file.id">
                <button class="icon-btn green" title="确认" @click="confirmRename()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg></button>
                <button class="icon-btn" title="取消" @click="renamingId=null"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
              </template>
              <template v-else>
                <button class="icon-btn" title="重命名" @click="startRename(file)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg></button>
                <button class="icon-btn" title="预览" @click="openPreview(file)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button>
                <button class="icon-btn" title="历史" @click="openVersions(file)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></button>
                <button class="icon-btn" title="分享" @click="handleShare(file)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 3.9M15.4 6.6l-6.8 3.9"/></svg></button>
                <button class="icon-btn" title="评论" @click="openComments(file)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></button>
                <button class="icon-btn primary" title="下载" @click="handleDownload(file)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg></button>
              </template>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!folders.length && !files.length" class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1" opacity="0.3"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>
          <h3>暂无资源</h3>
          <p>此文件夹为空，上传第一个文件吧</p>
          <button class="btn btn-primary" @click="showUpload = true">上传资源</button>
        </div>

        <!-- 分页 -->
        <div v-if="totalPages > 1" class="pagination-bar">
          <button class="page-btn" :disabled="page <= 1" @click="page--; loadResources()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg>
            上一页
          </button>
          <div class="page-dots">
            <template v-for="p in totalPages" :key="p">
              <button v-if="p === 1 || p === totalPages || Math.abs(p - page) <= 2" class="page-num" :class="{ active: p === page }" @click="page = p; loadResources()">{{ p }}</button>
              <span v-else-if="Math.abs(p - page) === 3" class="page-ellipsis">…</span>
            </template>
          </div>
          <button class="page-btn" :disabled="page >= totalPages" @click="page++; loadResources()">
            下一页
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
          </button>
        </div>
      </template>

      <div v-if="!isLoggedIn" class="login-prompt">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1.5" opacity="0.3"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <p>请先登录后访问资源中心</p>
      </div>
    </div>

    <!-- 以下所有弹窗保持不变 (Teleport modals) -->
    <Teleport to="body">
      <transition name="modal">
      <div v-if="showUpload" class="modal-layer" @click.self="showUpload = false">
        <div class="modal-panel">
          <div class="modal-top">
            <h3>上传资源</h3>
            <button class="modal-x" @click="showUpload = false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
          </div>
          <div class="modal-mid">
            <div class="upload-zone" :class="{ on: uploadDragover }" @drop.prevent="handleUploadDrop" @dragover.prevent="uploadDragover=true" @dragleave="uploadDragover=false" @click="$refs.fileInput.click()">
              <input ref="fileInput" type="file" @change="handleFileSelect" style="display:none" />
              <template v-if="uploadFile">
                <span v-html="iconSvg(uploadFile.name.split('.').pop(), 40)"></span>
                <strong>{{ uploadFile.name }}</strong>
                <span class="text-muted">{{ formatSize(uploadFile.size) }}</span>
              </template>
              <template v-else>
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
                <span>拖拽文件到此处或点击选择</span>
              </template>
            </div>
            <div class="modal-fields">
              <label class="m-field"><span>分类</span><select v-model="uploadForm.category"><option value="">选择分类</option><option v-for="c in categories" :key="c" :value="c">{{ c }}</option></select></label>
              <label class="m-field"><span>标签（逗号分隔）</span><input v-model="uploadForm.tags" placeholder="标签1, 标签2" /></label>
              <label class="m-field full"><span>描述</span><textarea v-model="uploadForm.description" rows="2" placeholder="文件描述..."></textarea></label>
            </div>
            <div v-if="uploading" class="upload-progress">
              <div class="progress-track"><div class="progress-bar" :style="{width:uploadProgress+'%'}"></div></div>
              <span class="progress-text">{{ uploadProgress }}%</span>
            </div>
          </div>
          <div class="modal-bot">
            <button class="btn btn-outline" @click="showUpload = false" :disabled="uploading">取消</button>
            <button class="btn btn-primary" @click="handleUpload" :disabled="!uploadFile || uploading">{{ uploading ? '上传中...' : '上传' }}</button>
          </div>
        </div>
      </div>
      </transition>
    </Teleport>

    <Teleport to="body">
      <transition name="modal">
      <div v-if="showCreateFolder" class="modal-layer" @click.self="showCreateFolder = false">
        <div class="modal-panel modal-sm">
          <div class="modal-top"><h3>新建文件夹</h3><button class="modal-x" @click="showCreateFolder = false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
          <div class="modal-mid"><label class="m-field"><span>文件夹名称</span><input v-model="folderName" placeholder="输入名称..." @keyup.enter="handleCreateFolder" /></label></div>
          <div class="modal-bot"><button class="btn btn-outline" @click="showCreateFolder = false">取消</button><button class="btn btn-primary" @click="handleCreateFolder" :disabled="!folderName.trim()">创建</button></div>
        </div>
      </div>
      </transition>
    </Teleport>

    <Teleport to="body">
      <div v-if="imagePreview" class="viewer-mask" @click.self="imagePreview=null">
        <button class="viewer-x" @click="imagePreview=null"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
        <button v-if="imageIndex > 0" class="viewer-nav left" @click="imageIndex--;loadImage()"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg></button>
        <img :src="imagePreview.url" :style="{transform:`scale(${imageZoom})`}" class="viewer-img" draggable="false" />
        <button v-if="imageIndex < imageFiles.length-1" class="viewer-nav right" @click="imageIndex++;loadImage()"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg></button>
        <div class="viewer-ctrl">
          <button @click="imageZoom=Math.max(0.2,imageZoom-0.25)">−</button>
          <span>{{ Math.round(imageZoom*100) }}%</span>
          <button @click="imageZoom=Math.min(5,imageZoom+0.25)">+</button>
          <button @click="imageZoom=1">1:1</button>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <div v-if="previewTarget" class="preview-overlay" @click.self="previewTarget=null">
        <div class="preview-toolbar">
          <span class="preview-fname">{{ previewTarget.original_name || previewTarget.name }}</span>
          <div class="preview-toolbar-actions">
            <button class="preview-tbtn" @click="handleDownload(previewTarget)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg> 下载</button>
            <button class="preview-tbtn close" @click="previewTarget=null"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
          </div>
        </div>
        <div class="preview-stage">
          <div v-if="previewLoading" class="preview-spin"><div class="spinner"></div></div>
          <template v-else-if="previewData">
            <iframe v-if="previewData.type==='pdf'&&previewPdfBlob" :src="previewPdfBlob" class="preview-pdf-frame"></iframe>
            <div v-else-if="previewData.type==='pdf'&&!previewPdfBlob" class="preview-na">加载PDF失败</div>
            <div v-else-if="previewData.type==='markdown'" v-html="renderMarkdown(previewData.content)" class="preview-md-box"></div>
            <div v-else-if="previewData.type==='text'" class="preview-code-box">
              <div class="code-header">{{ (previewTarget.file_ext||'').toUpperCase() }}</div>
              <pre><code>{{ previewData.content }}</code></pre>
            </div>
            <div v-else class="preview-na">
              <span class="preview-na-icon" v-html="iconSvg(previewTarget.file_ext, 48)"></span>
              <p>{{ previewTarget.original_name || previewTarget.name }}</p>
              <p class="text-muted">{{ formatSize(previewTarget.file_size) }} · 不支持在线预览</p>
              <button class="btn btn-primary" @click="handleDownload(previewTarget)">下载文件</button>
            </div>
          </template>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <transition name="modal">
      <div v-if="versionTarget" class="modal-layer" @click.self="versionTarget=null">
        <div class="modal-panel">
          <div class="modal-top"><h3>版本历史</h3><button class="modal-x" @click="versionTarget=null"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
          <div class="modal-mid">
            <p class="version-filename">{{ versionTarget.original_name || versionTarget.name }}</p>
            <div v-if="versionLoading" class="loading-state"><div class="spinner"></div></div>
            <div v-else-if="!versionList.length" class="empty-mini">暂无历史版本</div>
            <div v-else class="version-list">
              <div v-for="v in versionList" :key="v.id" class="version-row">
                <span class="v-badge">v{{ v.version }}</span>
                <span class="v-info">{{ formatSize(v.file_size) }} · {{ v.uploader_name||'-' }} · {{ formatDate(v.created_at) }}</span>
                <button class="btn btn-outline btn-sm" @click="handleRestoreVersion(v.id)">恢复此版本</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      </transition>
    </Teleport>

    <Teleport to="body">
      <transition name="modal">
      <div v-if="shareModalVisible" class="modal-layer" @click.self="shareModalVisible=false">
        <div class="modal-panel modal-sm">
          <div class="modal-top"><h3>分享链接</h3><button class="modal-x" @click="shareModalVisible=false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
          <div class="modal-mid share-modal">
            <div class="share-url-row">
              <input :value="shareModalUrl" readonly class="share-url" @click="$event.target.select()" />
              <button class="btn btn-primary" @click="copyShareUrl">复制</button>
            </div>
            <img v-if="shareModalUrl" :src="'https://api.qrserver.com/v1/create-qr-code/?size=180x180&data='+encodeURIComponent(shareModalUrl)" class="share-qr" />
            <p class="share-hint">扫码或复制链接分享给其他人</p>
          </div>
        </div>
      </div>
      </transition>
    </Teleport>

    <Teleport to="body">
      <transition name="modal">
      <div v-if="commentTarget" class="modal-layer" @click.self="commentTarget=null">
        <div class="modal-panel">
          <div class="modal-top"><h3>评论</h3><button class="modal-x" @click="commentTarget=null"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
          <div class="modal-mid">
            <p class="version-filename">{{ commentTarget.original_name || commentTarget.name }}</p>
            <div class="comment-box">
              <textarea v-model="commentText" placeholder="写下你的评论..." rows="3" @keyup.ctrl.enter="submitComment"></textarea>
              <button class="btn btn-primary btn-sm" @click="submitComment" :disabled="!commentText.trim()">发送</button>
            </div>
            <div v-if="commentLoading" class="loading-state"><div class="spinner"></div></div>
            <div v-else-if="!commentList.length" class="empty-mini">暂无评论</div>
            <div v-else class="comment-list">
              <div v-for="c in commentList" :key="c.id" class="comment-card">
                <div class="c-avatar">{{ (c.user_name||'?')[0] }}</div>
                <div class="c-body">
                  <div class="c-meta"><strong>{{ c.user_name||'匿名' }}</strong><span>{{ formatDate(c.created_at) }}</span></div>
                  <div class="c-text">{{ c.content }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { getResources, getResourceTags, getResourceStats, uploadResource, createFolder as apiCreateFolder, downloadResource, batchDownloadResources, previewResource as apiPreview, updateResource, getFolders, getResourceVersions, restoreVersion, createShareLink, removeShareLink, getComments, addComment } from '@/services/api'
import { isUserLoggedIn } from '@/services/api'
import { marked } from 'marked'

const ICON_COLORS = { folder:'#f5a623', pdf:'#e74c3c', doc:'#2b7cd3', docx:'#2b7cd3', rtf:'#2b7cd3', xls:'#217346', xlsx:'#217346', csv:'#217346', ppt:'#d04423', pptx:'#d04423', jpg:'#27ae60', jpeg:'#27ae60', png:'#27ae60', gif:'#27ae60', webp:'#27ae60', svg:'#27ae60', zip:'#e67e22', rar:'#e67e22', '7z':'#e67e22', tar:'#e67e22', gz:'#e67e22', py:'#3572a5', js:'#f1e05a', ts:'#3178c6', html:'#e34c26', css:'#563d7c', json:'#292929', txt:'#6b5e52', md:'#6b5e52', mp4:'#9b59b6', mp3:'#9b59b6' }

function iconSvg(ext, size=20) {
  const type=(ext||'').toLowerCase(); const color=ICON_COLORS[type]||'#8b7355'
  if(type==='folder') return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none"><path d="M2 6C2 4.9 2.9 4 4 4h5l2 3h9c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6Z" fill="${color}"/></svg>`
  const img=['jpg','jpeg','png','gif','webp','svg']; const arc=['zip','rar','7z','tar','gz']; const cod=['py','js','ts','html','css','json','yaml','xml','sql','sh','java','c','cpp','go','rs']
  let s='F'; if(img.includes(type)) s='🖼'; else if(arc.includes(type)) s='📦'; else if(['xls','xlsx','csv'].includes(type)) s='📊'; else if(['ppt','pptx'].includes(type)) s='📑'; else if(['mp4','mp3','wav'].includes(type)) s='▶'; else if(type==='pdf') s='PDF'; else if(cod.includes(type)) s='</>'; else if(['doc','docx','rtf','txt','md'].includes(type)) s='A'
  const fs=s.length>2?'7':'10'
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none"><rect x="4" y="2" width="16" height="20" rx="2" fill="${color}" opacity=".15"/><rect x="4" y="2" width="16" height="20" rx="2" stroke="${color}" stroke-width="1.5"/><text x="12" y="15" text-anchor="middle" font-size="${fs}" font-weight="600" fill="${color}">${s}</text></svg>`
}

const isLoggedIn = computed(()=>isUserLoggedIn())
const loading=ref(false), search=ref(''), filterCategory=ref(''), filterTag=ref(''), currentFolder=ref(null), breadcrumb=ref([]), folders=ref([]), files=ref([]), categories=ref([]), tags=ref([]), page=ref(1), totalPages=ref(1), stats=ref(null)
const sortKey=ref('date'), sortDir=ref('desc')
function toggleSort(k){ if(sortKey.value===k) sortDir.value=sortDir.value==='asc'?'desc':'asc'; else{sortKey.value=k;sortDir.value='asc'} }
const sortedFolders=computed(()=>sortItems(folders.value))
const sortedFiles=computed(()=>sortItems(files.value))
function sortItems(arr){ return [...arr].sort((a,b)=>{ let va,vb; if(sortKey.value==='name'){va=(a.name||'').toLowerCase();vb=(b.name||'').toLowerCase()} else if(sortKey.value==='size'){va=a.file_size||0;vb=b.file_size||0} else{va=a.updated_at||a.created_at||'';vb=b.updated_at||b.created_at||''}; if(va<vb) return sortDir.value==='asc'?-1:1; if(va>vb) return sortDir.value==='asc'?1:-1; return 0 })}

const selectedIds=ref(new Set())
const isAllChecked=computed(()=>{ const all=[...folders.value.map(f=>'f-'+f.id),...files.value.map(f=>'r-'+f.id)]; return all.length>0&&all.every(id=>selectedIds.value.has(id)) })
function toggleSelect(id){ const s=new Set(selectedIds.value); s.has(id)?s.delete(id):s.add(id); selectedIds.value=s }
function toggleSelectAll(){ if(isAllChecked.value){selectedIds.value=new Set();return}; const all=[...folders.value.map(f=>'f-'+f.id),...files.value.map(f=>'r-'+f.id)]; selectedIds.value=new Set(all) }

const showUpload=ref(false), uploadFile=ref(null), uploading=ref(false), uploadProgress=ref(0), uploadDragover=ref(false), pageDragover=ref(false), uploadForm=ref({category:'',tags:'',description:''})
const showCreateFolder=ref(false), folderName=ref('')
const previewTarget=ref(null), previewData=ref(null), previewLoading=ref(false), previewPdfBlob=ref(null)
const imagePreview=ref(null), imageIndex=ref(0), imageZoom=ref(1)
const imageFiles=computed(()=>files.value.filter(f=>['jpg','jpeg','png','gif','webp','svg','bmp','ico'].includes((f.file_ext||'').toLowerCase())))
function loadImage(){ const f=imageFiles.value[imageIndex.value]; if(f){imagePreview.value={url:f.file_url};imageZoom.value=1} }
function handleZoom(e){ imageZoom.value=Math.max(0.2,Math.min(5,imageZoom.value+(e.deltaY>0?-0.15:0.15))) }
const moveTarget=ref(null), moveFolderId=ref(''), allFolders=ref([])
const versionTarget=ref(null), versionList=ref([]), versionLoading=ref(false)
const commentTarget=ref(null), commentList=ref([]), commentText=ref(''), commentLoading=ref(false)
const renamingId=ref(null), renamingName=ref('')
const shareModalVisible=ref(false), shareModalUrl=ref('')

function startRename(item){ renamingId.value=item.id; renamingName.value=item.original_name||item.name; nextTick(()=>{ const el=document.querySelector('.rename-input'); if(el) el.focus() }) }
function confirmRename(){ const id=renamingId.value; const n=renamingName.value.trim(); renamingId.value=null; if(!id||!n) return; updateResource(id,{name:n}).then(()=>loadResources()).catch(e=>{alert(e.message||'重命名失败');loadResources()}) }
function isImageExt(ext){ return ['jpg','jpeg','png','gif','webp','svg','bmp','ico'].includes((ext||'').toLowerCase()) }
function formatSize(b){ if(!b) return '-'; const u=['B','KB','MB','GB']; let i=0; while(b>=1024&&i<u.length-1){b/=1024;i++}; return `${b.toFixed(i>0?1:0)} ${u[i]}` }
function formatDate(iso){ if(!iso) return '-'; const d=new Date(iso+'Z'); const p=n=>String(n).padStart(2,'0'); return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}` }
function renderMarkdown(c){ try{return marked(c||'')}catch{return''} }

let st=null
function debouncedLoad(){ clearTimeout(st); st=setTimeout(()=>{page.value=1;loadResources()},300) }

async function loadResources(){
  if(!isLoggedIn.value) return; loading.value=true
  try{
    const params={page:page.value,per_page:20}; if(currentFolder.value) params.parent_id=currentFolder.value; if(search.value) params.search=search.value; if(filterCategory.value) params.category=filterCategory.value; if(filterTag.value) params.tag=filterTag.value
    const [data,td]=await Promise.all([getResources(params),tags.value.length?Promise.resolve({tags:tags.value}):getResourceTags().catch(()=>({tags:[]}))])
    folders.value=data.items.filter(r=>r.is_folder); files.value=data.items.filter(r=>!r.is_folder); totalPages.value=data.pages; breadcrumb.value=data.breadcrumb||[]; if(data.categories) categories.value=data.categories; if(td.tags) tags.value=td.tags
    try{const s=await getResourceStats(currentFolder.value);stats.value={totalFiles:s.total_files,totalSize:s.total_size}}catch{const total=data.total||0;const sz=[...folders.value,...files.value].reduce((a,r)=>a+(r.file_size||0),0);stats.value={totalFiles:total,totalSize:sz}}
  }catch(e){console.error(e)}finally{loading.value=false}
}

function navigateTo(folderId){ currentFolder.value=folderId; page.value=1; search.value=''; filterCategory.value=''; filterTag.value=''; loadResources() }
function handlePageDrop(e){ pageDragover.value=false; const f=e.dataTransfer?.files?.[0]; if(f){uploadFile.value=f;showUpload.value=true} }
function handleUploadDrop(e){ uploadDragover.value=false; const f=e.dataTransfer?.files?.[0]; if(f) uploadFile.value=f }
function handleFileSelect(e){ const f=e.target.files?.[0]; if(f) uploadFile.value=f }

async function handleUpload(){
  if(!uploadFile.value) return; uploading.value=true; uploadProgress.value=0
  const fd=new FormData(); fd.append('file',uploadFile.value); if(currentFolder.value) fd.append('parent_id',currentFolder.value); if(uploadForm.value.category) fd.append('category',uploadForm.value.category); if(uploadForm.value.tags) fd.append('tags',JSON.stringify(uploadForm.value.tags.split(',').map(t=>t.trim()).filter(Boolean))); if(uploadForm.value.description) fd.append('description',uploadForm.value.description)
  const xhr=new XMLHttpRequest(); xhr.open('POST',`${import.meta.env.VITE_API_BASE||'/api'}/resources/upload`); const tk=localStorage.getItem('xingyu_user_token'); if(tk) xhr.setRequestHeader('Authorization',`Bearer ${tk}`)
  xhr.upload.onprogress=e=>{ if(e.lengthComputable) uploadProgress.value=Math.round(e.loaded/e.total*100) }
  xhr.onload=()=>{ uploading.value=false; if(xhr.status>=200&&xhr.status<300){showUpload.value=false;uploadFile.value=null;uploadForm.value={category:'',tags:'',description:''};loadResources()}else{try{alert(JSON.parse(xhr.responseText).message||'上传失败')}catch{alert('上传失败')}}}
  xhr.onerror=()=>{uploading.value=false;alert('网络错误')}; xhr.send(fd)
}
async function handleCreateFolder(){ if(!folderName.value.trim()) return; try{await apiCreateFolder({name:folderName.value.trim(),parent_id:currentFolder.value});showCreateFolder.value=false;folderName.value='';loadResources()}catch(e){alert(e.message||'创建失败')} }
async function handleDownload(file){ try{const r=await fetch(`${import.meta.env.VITE_API_BASE||'/api'}/resources/${file.id}/download`,{headers:{Authorization:'Bearer '+localStorage.getItem('xingyu_user_token')}}); if(!r.ok){const d=await r.json().catch(()=>({}));alert(d.message||'下载失败');return}; const b=await r.blob(); const a=document.createElement('a'); a.href=URL.createObjectURL(b); const cd=r.headers.get('Content-Disposition')||''; const m=cd.match(/filename\*=UTF-8''(.+)/i); a.download=m?decodeURIComponent(m[1]):(file.original_name||file.name); a.click(); URL.revokeObjectURL(a.href)}catch(e){alert('下载失败')} }
async function handleBatchDownload(){ const fIds=[...selectedIds.value].filter(id=>id.startsWith('r-')).map(id=>parseInt(id.replace('r-',''))); const dIds=[...selectedIds.value].filter(id=>id.startsWith('f-')).map(id=>parseInt(id.replace('f-',''))); if(!fIds.length&&!dIds.length){alert('请先选择');return}; try{await batchDownloadResources(fIds,dIds)}catch(e){alert(e.message||'失败')} }
async function openPreview(file){ const ext=(file.file_ext||'').toLowerCase(); if(isImageExt(ext)){ const idx=imageFiles.value.findIndex(f=>f.id===file.id); imageIndex.value=idx>=0?idx:0; imagePreview.value={url:file.file_url}; imageZoom.value=1; return }; previewTarget.value=file; previewLoading.value=true; previewData.value=null; previewPdfBlob.value=null; try{const d=await apiPreview(file.id); previewData.value=d; if(d.type==='pdf'){ try{const r=await fetch(d.url,{headers:{'Authorization':'Bearer '+localStorage.getItem('xingyu_user_token')}}); if(r.ok){const b=await r.blob(); previewPdfBlob.value=URL.createObjectURL(b)} }catch{}} }catch{previewData.value={type:'unsupported'}}finally{previewLoading.value=false} }
async function openVersions(file){ versionTarget.value=file; versionLoading.value=true; versionList.value=[]; try{const d=await getResourceVersions(file.id); versionList.value=d.versions||[]}catch{versionList.value=[]}finally{versionLoading.value=false} }
async function handleRestoreVersion(id){ if(!confirm('确定恢复？')) return; try{await restoreVersion(versionTarget.value.id,id);versionTarget.value=null;loadResources()}catch(e){alert(e.message||'恢复失败')} }
async function handleShare(file){ try{const d=await createShareLink(file.id); shareModalUrl.value=`${window.location.origin}/share/${d.token}`; shareModalVisible.value=true}catch(e){alert(e.message||'失败')} }
function copyShareUrl(){ var t=document.createElement('textarea'); t.value=shareModalUrl.value; t.style.position='fixed'; t.style.left='-9999px'; document.body.appendChild(t); t.select(); try{document.execCommand('copy');alert('链接已复制')}catch(e){alert('手动复制：'+shareModalUrl.value)}; document.body.removeChild(t) }
async function openComments(file){ commentTarget.value=file;commentLoading.value=true;commentText.value='';try{const d=await getComments(file.id);commentList.value=d.comments||[]}catch{commentList.value=[]}finally{commentLoading.value=false} }
async function submitComment(){ if(!commentText.value.trim()) return; try{const d=await addComment(commentTarget.value.id,commentText.value.trim());commentList.value.unshift(d.comment);commentText.value=''}catch(e){alert(e.message||'评论失败')} }
async function openMove(item){ moveTarget.value=item;moveFolderId.value='';try{const d=await getAdminFolders();allFolders.value=(d.folders||[]).filter(f=>f.id!==item.id)}catch{allFolders.value=[]} }
async function handleMove(){ try{await moveResource(moveTarget.value.id,moveFolderId.value?parseInt(moveFolderId.value):null);moveTarget.value=null;loadResources()}catch(e){alert(e.message||'移动失败')} }

function handleKeydown(e){ if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) return
  if(e.key==='Delete'&&selectedIds.value.size>0){ e.preventDefault(); handleBatchDelete() }
  if((e.ctrlKey||e.metaKey)&&e.key==='a'){ e.preventDefault(); toggleSelectAll() }
  if(e.key==='Enter'&&selectedIds.value.size===1){ const id=[...selectedIds.value][0]; if(id.startsWith('f-')){ e.preventDefault(); navigateTo(parseInt(id.replace('f-',''))) } }
}
async function handleBatchDelete(){ if(!confirm(`删除${selectedIds.value.size}项？`)) return; for(const id of [...selectedIds.value]){ try{const{deleteResource}=await import('@/services/api');await deleteResource(parseInt(id.replace(/[fr]-/,'')))}catch{} }; selectedIds.value=new Set(); loadResources() }

onMounted(()=>{ if(isLoggedIn.value) loadResources(); window.addEventListener('keydown',handleKeydown) })
onUnmounted(()=>{ window.removeEventListener('keydown',handleKeydown) })
watch(isLoggedIn,v=>{ if(v) loadResources() })
watch(previewTarget,v=>{ if(!v&&previewPdfBlob.value){ URL.revokeObjectURL(previewPdfBlob.value); previewPdfBlob.value=null } })
</script>

<style scoped>
/* ===== 布局 ===== */
.page-view{min-height:100vh;padding:80px 0 60px}
.container{max-width:1120px;margin:0 auto;padding:0 24px}

/* ===== 头部 ===== */
.page-header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:16px}
.header-left h1{display:flex;align-items:center;gap:10px;font-family:var(--font-heading);font-size:26px;margin:0;letter-spacing:-0.01em}
.header-icon{flex-shrink:0}
.page-subtitle{color:var(--text-muted);font-size:13px;margin:6px 0 0 0}
.header-stats{display:flex;align-items:center;gap:16px;background:white;border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:10px 20px}
.stat-item{display:flex;flex-direction:column;align-items:center;gap:2px}
.stat-value{font-family:var(--font-heading);font-size:18px;font-weight:700;color:var(--warm-terracotta)}
.stat-label{font-size:11px;color:var(--text-muted)}
.stat-divider{width:1px;height:32px;background:var(--glass-border)}

/* ===== 工具栏 ===== */
.toolbar-card{background:white;border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:12px 16px;margin-bottom:14px;box-shadow:var(--shadow-sm)}
.toolbar-main{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.search-wrap{display:flex;align-items:center;gap:8px;flex:1;min-width:200px;background:var(--bg-soft);border:1px solid transparent;border-radius:var(--radius-md);padding:0 12px;transition:all .2s}
.search-wrap:focus-within{background:white;border-color:var(--warm-terracotta);box-shadow:0 0 0 3px rgba(192,96,64,.08)}
.search-icon{color:var(--text-muted);flex-shrink:0}
.search-input{flex:1;border:none;background:none;padding:9px 0;font-size:13px;outline:none;color:var(--text-primary)}
.search-input::placeholder{color:var(--text-muted)}
.search-clear{background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:16px;padding:2px;line-height:1}
.filter-group{display:flex;gap:8px}
.filter-select{padding:8px 12px;border:1px solid var(--glass-border);border-radius:var(--radius-md);font-size:12px;background:white;color:var(--text-primary);cursor:pointer;min-width:100px}
.action-group{display:flex;gap:8px;margin-left:auto}

/* ===== 批量栏 ===== */
.batch-bar{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;background:linear-gradient(135deg,rgba(192,96,64,.08),rgba(212,146,10,.05));border:1px solid rgba(192,96,64,.15);border-radius:var(--radius-lg);margin-bottom:14px}
.batch-left{display:flex;align-items:center;gap:10px}
.batch-badge{background:var(--warm-terracotta);color:white;font-weight:700;font-size:13px;min-width:26px;height:26px;border-radius:13px;display:flex;align-items:center;justify-content:center}
.batch-text{font-size:13px;font-weight:500}
.batch-actions{display:flex;gap:8px}
.btn-text{background:none;border:none;color:var(--text-muted);font-size:12px;cursor:pointer;padding:6px 12px;border-radius:6px}
.btn-text:hover{color:var(--text-primary);background:rgba(0,0,0,.04)}

/* ===== 面包屑 ===== */
.breadcrumb-bar{display:flex;align-items:center;gap:4px;margin-bottom:12px;flex-wrap:wrap}
.breadcrumb-link{display:inline-flex;align-items:center;gap:5px;padding:5px 10px;border:none;background:none;font-size:12px;color:var(--text-muted);cursor:pointer;border-radius:6px;transition:all .15s}
.breadcrumb-link:hover{color:var(--warm-terracotta);background:rgba(192,96,64,.04)}
.breadcrumb-link.active{color:var(--text-primary);font-weight:600;background:var(--bg-soft)}
.breadcrumb-chevron{color:var(--text-muted);flex-shrink:0}

/* ===== 列表头 ===== */
.list-header{display:flex;align-items:center;padding:10px 16px;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em;background:var(--bg-soft);border-radius:var(--radius-lg) var(--radius-lg) 0 0;border:1px solid var(--glass-border);border-bottom:none}
.list-body{background:white;border:1px solid var(--glass-border);border-top:none;border-radius:0 0 var(--radius-lg) var(--radius-lg);overflow:visible}
.list-body .list-row:last-child{border-radius:0 0 var(--radius-lg) var(--radius-lg)}
.lh-check{width:36px;flex-shrink:0}
.lh-name{flex:1;min-width:0}
.lh-size{width:90px;text-align:right;flex-shrink:0}
.lh-uploader{width:100px;text-align:center;flex-shrink:0}
.lh-date{width:145px;text-align:center;flex-shrink:0}
.lh-actions{width:180px;text-align:right;flex-shrink:0;padding-right:8px}
.sortable{cursor:pointer;user-select:none;transition:color .15s}
.sortable:hover{color:var(--warm-terracotta)}
.sort-arrow{font-size:9px;opacity:0;transition:all .2s}
.sort-arrow.active{opacity:.5}
.sort-arrow.down{transform:rotate(180deg)}

/* ===== 行 ===== */
.list-row{display:flex;align-items:center;padding:12px 16px;border-bottom:1px solid rgba(0,0,0,.03);transition:all .15s}
.list-row:last-child{border-bottom:none}
.list-row:hover{background:linear-gradient(90deg,rgba(192,96,64,.02) 0%,transparent 50%)}
.list-row.folder{cursor:pointer}
.list-row.folder:hover{background:linear-gradient(90deg,rgba(245,166,35,.06) 0%,transparent 50%)}
.lr-check{width:36px;flex-shrink:0}
.lr-check input{cursor:pointer;accent-color:var(--warm-terracotta)}
.lr-name{flex:1;min-width:0;display:flex;align-items:center;gap:10px}
.lr-icon{flex-shrink:0;display:flex;align-items:center}
.lr-thumb{width:36px;height:36px;object-fit:cover;border-radius:6px;border:1px solid var(--glass-border);flex-shrink:0}
.lr-name-inner{display:flex;align-items:center;gap:8px;min-width:0}
.lr-name-wrap{position:relative}
.lr-text{font-size:13px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}
.lr-tag{font-size:10px;padding:2px 8px;background:rgba(192,96,64,.08);color:var(--warm-terracotta);border-radius:999px;font-weight:500;flex-shrink:0}
.lr-size{width:90px;text-align:right;font-size:12px;color:var(--text-muted);flex-shrink:0}
.lr-uploader{width:100px;text-align:center;font-size:12px;color:var(--text-muted);flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lr-date{width:145px;text-align:center;font-size:12px;color:var(--text-muted);flex-shrink:0}
.lr-actions{width:180px;display:flex;justify-content:flex-end;gap:2px;flex-shrink:0}

/* ===== 图标按钮 ===== */
.icon-btn{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border:none;background:none;color:var(--text-muted);cursor:pointer;border-radius:8px;transition:all .15s}
.icon-btn:hover{background:var(--bg-soft);color:var(--warm-terracotta)}
.icon-btn.primary{color:var(--warm-terracotta);background:rgba(192,96,64,.08)}
.icon-btn.primary:hover{background:rgba(192,96,64,.15)}
.rename-input{padding:4px 8px;border:1.5px solid var(--warm-terracotta);border-radius:6px;font-size:13px;width:200px;outline:none;background:white}

/* ===== 悬浮卡片 ===== */
.hover-card{display:none;position:absolute;left:-10px;bottom:100%;margin-bottom:8px;z-index:200;background:white;border:1px solid var(--glass-border);border-radius:var(--radius-md);padding:14px 18px;min-width:280px;box-shadow:var(--shadow-xl);pointer-events:none}
.lr-name-wrap:hover .hover-card{display:block}
.hover-title{font-size:13px;font-weight:600;margin-bottom:4px;word-break:break-all}
.hover-tag{display:inline-block;font-size:10px;padding:2px 8px;background:rgba(192,96,64,.08);color:var(--warm-terracotta);border-radius:999px;margin-bottom:6px}
.hover-desc{font-size:12px;color:var(--text-secondary);margin-bottom:8px;line-height:1.5;max-height:48px;overflow:hidden}
.hover-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;font-size:11px;color:var(--text-muted);margin-bottom:6px}
.hover-tags{display:flex;gap:4px;flex-wrap:wrap}
.tag-sm{font-size:10px;padding:2px 8px;background:var(--bg-soft);border-radius:999px;color:var(--text-secondary)}

/* ===== 分页 ===== */
.pagination-bar{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:24px}
.page-btn{display:inline-flex;align-items:center;gap:4px;padding:7px 16px;border:1px solid var(--glass-border);background:white;border-radius:var(--radius-md);font-size:12px;cursor:pointer;transition:all .15s}
.page-btn:hover:not(:disabled){border-color:var(--warm-terracotta);color:var(--warm-terracotta)}
.page-btn:disabled{opacity:.4;cursor:not-allowed}
.page-dots{display:flex;gap:4px}
.page-num{width:34px;height:34px;border:1px solid transparent;background:none;border-radius:var(--radius-md);font-size:13px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s}
.page-num:hover{background:var(--bg-soft)}
.page-num.active{background:var(--warm-terracotta);color:white;font-weight:600}
.page-ellipsis{width:34px;height:34px;display:flex;align-items:center;justify-content:center;color:var(--text-muted)}

/* ===== 空/加载/登录 ===== */
.empty-state{text-align:center;padding:80px 20px}
.empty-state h3{font-family:var(--font-heading);font-size:18px;margin:16px 0 6px}
.empty-state p{color:var(--text-muted);margin:0 0 20px;font-size:13px}
.loading-state{display:flex;flex-direction:column;align-items:center;gap:12px;padding:80px 20px;color:var(--text-muted);font-size:13px}
.login-prompt{text-align:center;padding:80px 0;color:var(--text-muted)}
.login-prompt p{margin-top:12px;font-size:14px}
.spinner{width:28px;height:28px;border:3px solid var(--glass-border);border-top-color:var(--warm-terracotta);border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* ===== 全局拖拽 ===== */
.global-drop-overlay{position:fixed;inset:0;background:rgba(192,96,64,.06);border:3px dashed var(--warm-terracotta);z-index:999;display:flex;align-items:center;justify-content:center;pointer-events:none}
.global-drop-content{background:white;padding:40px 56px;border-radius:var(--radius-xl);box-shadow:var(--shadow-xl);display:flex;flex-direction:column;align-items:center;gap:16px;font-size:16px;font-weight:500;color:var(--warm-terracotta)}

/* ===== 模态弹窗 ===== */
.modal-layer{position:fixed;inset:0;background:rgba(0,0,0,.45);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px}
.modal-panel{background:white;border-radius:var(--radius-xl);width:100%;max-width:520px;max-height:88vh;display:flex;flex-direction:column;box-shadow:0 25px 60px rgba(0,0,0,.15)}
.modal-sm{max-width:400px}
.modal-lg{max-width:800px}
.modal-top{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid var(--glass-border)}
.modal-top h3{font-family:var(--font-heading);font-size:16px;font-weight:600;margin:0}
.modal-x{background:none;border:none;color:var(--text-muted);cursor:pointer;padding:4px;border-radius:6px;display:flex;transition:all .15s}
.modal-x:hover{background:var(--bg-soft);color:var(--text-primary)}
.modal-mid{padding:24px;overflow-y:auto;flex:1}
.modal-bot{display:flex;justify-content:flex-end;gap:8px;padding:14px 24px;border-top:1px solid var(--glass-border);background:var(--bg-soft)}

/* 上传 */
.upload-zone{border:2px dashed var(--glass-border);border-radius:var(--radius-lg);padding:40px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:20px;display:flex;flex-direction:column;align-items:center;gap:10px}
.upload-zone:hover,.upload-zone.on{border-color:var(--warm-terracotta);background:rgba(192,96,64,.02)}
.upload-progress{display:flex;align-items:center;gap:10px;margin-top:12px}
.progress-track{flex:1;height:6px;background:var(--bg-soft);border-radius:3px;overflow:hidden}
.progress-bar{height:100%;background:var(--grad-primary);border-radius:3px;transition:width .3s}
.progress-text{font-size:12px;color:var(--text-muted);min-width:36px;text-align:right}

/* 表单 */
.modal-fields{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.m-field{display:flex;flex-direction:column}
.m-field.full{grid-column:1/-1}
.m-field span{font-size:12px;font-weight:500;color:var(--text-muted);margin-bottom:5px}
.m-field input,.m-field select,.m-field textarea{padding:9px 12px;border:1px solid var(--glass-border);border-radius:var(--radius-md);font-size:13px;background:white;font-family:inherit;transition:border-color .15s}
.m-field input:focus,.m-field select:focus,.m-field textarea:focus{outline:none;border-color:var(--warm-terracotta);box-shadow:0 0 0 3px rgba(192,96,64,.06)}

/* 预览 */
/* 非图片预览全屏 */
.preview-overlay{position:fixed;inset:0;background:#f8f5f0;z-index:2000;display:flex;flex-direction:column}
.preview-toolbar{display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:52px;background:white;border-bottom:1px solid var(--glass-border);flex-shrink:0}
.preview-fname{font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:60%}
.preview-toolbar-actions{display:flex;gap:8px;align-items:center}
.preview-tbtn{display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border:1px solid var(--glass-border);background:white;border-radius:6px;font-size:12px;cursor:pointer;color:var(--text-primary);transition:all .15s}
.preview-tbtn:hover{background:var(--bg-soft)}
.preview-tbtn.close{border:none;background:none;padding:6px;font-size:14px}
.preview-tbtn.close:hover{background:var(--bg-soft)}
.preview-stage{flex:1;overflow:auto;display:flex;align-items:flex-start;justify-content:center;padding:24px}
.preview-spin{display:flex;align-items:center;justify-content:center;height:100%;width:100%}
.preview-pdf-frame{width:100%;height:100%;min-height:calc(100vh - 100px);border:none;border-radius:var(--radius-lg);background:white;box-shadow:var(--shadow-md)}
.preview-md-box{width:100%;max-width:900px;background:white;border-radius:var(--radius-lg);padding:40px 48px;box-shadow:var(--shadow-md);overflow:auto;max-height:calc(100vh - 100px)}
.preview-code-box{width:100%;max-width:1000px;background:#1e1e1e;border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-lg)}
.code-header{padding:8px 16px;font-size:11px;color:#999;background:#2d2d2d;font-family:var(--font-mono)}
.preview-code-box pre{padding:20px 24px;margin:0;overflow:auto;max-height:calc(100vh - 140px);color:#d4d4d4;font-size:13px;line-height:1.6;font-family:var(--font-mono);tab-size:4;white-space:pre-wrap;word-break:break-all}
.preview-na{text-align:center;color:var(--text-muted);padding:80px 20px;display:flex;flex-direction:column;align-items:center;gap:12px}
.preview-na-icon{margin-bottom:8px}

/* 版本 */
.version-filename{font-size:13px;color:var(--text-muted);margin-bottom:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.version-list{display:flex;flex-direction:column;gap:8px}
.version-row{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--bg-soft);border-radius:var(--radius-md)}
.v-badge{font-weight:700;font-size:12px;min-width:32px}
.v-info{flex:1;font-size:12px;color:var(--text-muted)}
.empty-mini{text-align:center;color:var(--text-muted);padding:24px 0;font-size:13px}

/* 分享 */
.share-modal{display:flex;flex-direction:column;align-items:center;gap:16px}
.share-url-row{display:flex;gap:8px;width:100%}
.share-url{flex:1;padding:9px 12px;border:1px solid var(--glass-border);border-radius:var(--radius-md);font-size:12px;background:var(--bg-soft);color:var(--text-primary)}
.share-qr{width:180px;height:180px;border-radius:var(--radius-md);border:1px solid var(--glass-border)}
.share-hint{font-size:12px;color:var(--text-muted)}

/* 评论 */
.comment-box{display:flex;gap:8px;margin-bottom:16px}
.comment-box textarea{flex:1;padding:10px 12px;border:1px solid var(--glass-border);border-radius:var(--radius-md);font-size:13px;resize:vertical;font-family:inherit;min-height:60px}
.comment-box textarea:focus{outline:none;border-color:var(--warm-terracotta)}
.comment-list{display:flex;flex-direction:column;gap:12px;max-height:350px;overflow-y:auto}
.comment-card{display:flex;gap:10px}
.c-avatar{width:34px;height:34px;border-radius:50%;background:var(--warm-terracotta);color:white;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;flex-shrink:0}
.c-body{flex:1;min-width:0}
.c-meta{display:flex;gap:10px;align-items:center;margin-bottom:4px}
.c-meta strong{font-size:13px}
.c-meta span{font-size:11px;color:var(--text-muted)}
.c-text{font-size:13px;line-height:1.6;color:var(--text-secondary);word-break:break-word}

/* 图片查看器 */
.viewer-mask{position:fixed;inset:0;background:rgba(0,0,0,.94);z-index:2000;display:flex;align-items:center;justify-content:center}
.viewer-x{position:absolute;top:16px;right:20px;background:none;border:none;cursor:pointer;z-index:10;padding:8px;border-radius:8px;transition:all .2s}
.viewer-x:hover{background:rgba(255,255,255,.1)}
.viewer-img{max-width:90vw;max-height:90vh;object-fit:contain;transition:transform .15s}
.viewer-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.1);border:none;cursor:pointer;padding:16px 10px;border-radius:12px;transition:all .2s;display:flex}
.viewer-nav:hover{background:rgba(255,255,255,.2)}
.viewer-nav.left{left:16px}
.viewer-nav.right{right:16px}
.viewer-ctrl{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;background:rgba(0,0,0,.7);padding:8px 18px;border-radius:999px}
.viewer-ctrl button{background:rgba(255,255,255,.15);border:none;color:white;padding:4px 14px;border-radius:6px;cursor:pointer;font-size:14px;transition:all .15s}
.viewer-ctrl button:hover{background:rgba(255,255,255,.25)}
.viewer-ctrl span{color:white;font-size:13px;min-width:44px;text-align:center}

/* 过渡 */
.fade-enter-active,.fade-leave-active{transition:all .2s}
.fade-enter-from,.fade-leave-to{opacity:0;transform:translateY(-4px)}
.modal-enter-active,.modal-leave-active{transition:all .2s}
.modal-enter-from,.modal-leave-to{opacity:0;transform:scale(.96)}

/* ===== 按钮 ===== */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:8px 18px;border-radius:var(--radius-md);font-size:13px;font-weight:500;cursor:pointer;border:none;transition:all .2s}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-primary{background:var(--grad-primary);color:white;box-shadow:0 2px 12px rgba(192,96,64,.2)}
.btn-primary:hover:not(:disabled){opacity:.9;box-shadow:0 4px 16px rgba(192,96,64,.3)}
.btn-outline{background:white;border:1px solid var(--glass-border);color:var(--text-primary)}
.btn-outline:hover:not(:disabled){border-color:var(--warm-terracotta);color:var(--warm-terracotta);background:rgba(192,96,64,.02)}
.btn-sm{padding:5px 12px;font-size:12px}
.text-muted{font-size:12px;color:var(--text-muted)}

@media (max-width:768px){
  .toolbar-main{flex-direction:column;align-items:stretch}
  .action-group{margin-left:0;justify-content:flex-end}
  .lh-uploader,.lh-date,.lr-uploader,.lr-date{display:none}
  .lh-actions{width:140px}.lr-actions{width:140px}
  .header-stats{display:none}
  .modal-fields{grid-template-columns:1fr}
}
</style>
